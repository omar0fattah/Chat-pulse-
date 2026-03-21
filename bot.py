import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiosqlite
from typing import Optional

# ==================== CONFIG ====================
TOKEN = os.environ.get('TOKEN') or os.environ.get('DISCORD_BOT_TOKEN')
DB_PATH = 'chatpulse.db'

# ==================== BOT SETUP ====================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ==================== DATABASE ====================
_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id INTEGER PRIMARY KEY,
    revive_channel_id INTEGER,
    revive_role_id INTEGER,
    revive_enabled INTEGER DEFAULT 1,
    last_revive_ts INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_questions_guild ON questions(guild_id);
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(_SCHEMA_SQL)
        await db.commit()

async def get_guild_config(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
        row = await cur.fetchone()
        await cur.close()
        if row:
            return dict(row)
    return {"guild_id": guild_id, "revive_channel_id": None, "revive_role_id": None, "revive_enabled": 1, "last_revive_ts": 0}

async def set_guild_config(guild_id: int, **kwargs):
    async with aiosqlite.connect(DB_PATH) as db:
        cfg = await get_guild_config(guild_id)
        cfg.update(kwargs)
        await db.execute(
            "INSERT OR REPLACE INTO guilds (guild_id, revive_channel_id, revive_role_id, revive_enabled, last_revive_ts) VALUES (?, ?, ?, ?, ?)",
            (
                guild_id,
                cfg.get("revive_channel_id"),
                cfg.get("revive_role_id"),
                cfg.get("revive_enabled"),
                cfg.get("last_revive_ts"),
            ),
        )
        await db.commit()

async def add_question(guild_id: int, author_id: int, content: str, ts: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO questions (guild_id, author_id, content, created_at) VALUES (?, ?, ?, ?)",
            (guild_id, author_id, content, ts),
        )
        await db.commit()
        return cur.lastrowid

async def get_questions_for_guild(guild_id: int, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, author_id, content, created_at FROM questions WHERE guild_id = ? ORDER BY created_at DESC LIMIT ?",
            (guild_id, limit),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

# ==================== BACKGROUND LOOP ====================
async def check_inactivity_loop(bot: commands.Bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM guilds WHERE revive_enabled = 1")
            rows = await cur.fetchall()
        now_ts = int(asyncio.get_event_loop().time())
        for row in rows:
            if row["revive_channel_id"] and now_ts - row["last_revive_ts"] > 24*60*60:
                channel = bot.get_channel(row["revive_channel_id"])
                if channel:
                    try:
                        await channel.send("🔔 Revive check — say something to keep this channel active!")
                        await set_guild_config(row["guild_id"], last_revive_ts=now_ts)
                    except Exception as e:
                        print(f"Failed to send revive: {e}")
        await asyncio.sleep(60)

# ==================== SLASH COMMANDS ====================
@tree.command(name="ping", description="Test if bot responds")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="setup_revive", description="Configure revive channel and role")
@app_commands.describe(channel="Channel to post revive messages", role="Role to mention (optional)")
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel, role: Optional[discord.Role] = None):
    await interaction.response.defer(thinking=True)
    await set_guild_config(interaction.guild_id, revive_channel_id=channel.id, revive_role_id=(role.id if role else None))
    await interaction.followup.send(
        f"✅ Revive set to {channel.mention}" + (f" and will mention {role.mention}" if role else ""),
        ephemeral=True
    )

@tree.command(name="revive_now", description="Trigger a manual revive")
async def revive_now(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    cfg = await get_guild_config(interaction.guild_id)
    channel = interaction.guild.get_channel(cfg.get("revive_channel_id"))
    if channel:
        await channel.send("🔔 Manual revive triggered — say hi!")
        await set_guild_config(interaction.guild_id, last_revive_ts=int(asyncio.get_event_loop().time()))
        await interaction.followup.send("✅ Revive message sent.", ephemeral=True)
    else:
        await interaction.followup.send("❌ No revive channel configured.", ephemeral=True)

@tree.command(name="list_questions", description="List recent stored questions")
async def list_questions(interaction: discord.Interaction, limit: Optional[int] = 10):
    await interaction.response.defer(thinking=True)
    questions = await get_questions_for_guild(interaction.guild_id, limit)
    if not questions:
        await interaction.followup.send("No questions found.", ephemeral=True)
        return
    lines = [f"**#{q['id']}** by <@{q['author_id']}> — {q['content'][:100]}" for q in questions]
    await interaction.followup.send("\n".join(lines), ephemeral=True)

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    await init_db()
    bot.loop.create_task(check_inactivity_loop(bot))
    await tree.sync()
    print(f"Bot ready: {bot.user}")

# ==================== RUN ====================
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ No bot token found in environment variables.")
