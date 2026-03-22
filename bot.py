# chatpulse_bot.py
import os, time, random, logging, asyncio, aiosqlite, re
from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands

# Config
TOKEN = os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("TOKEN")
DB_PATH = os.environ.get("DB_PATH", "chatpulse.db")
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("chatpulse")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Minimal DEFAULT_QUESTIONS (keep your full dict here)
DEFAULT_QUESTIONS = {"general": ["If you could have dinner with any fictional character, who?"]}

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(guild_id, name)
);
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS revive_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    inactivity_threshold INTEGER NOT NULL,
    last_message_ts INTEGER DEFAULT 0
);
"""

# Utilities using a single persistent connection
async def init_db(conn: aiosqlite.Connection):
    await conn.executescript(_SCHEMA_SQL)
    await conn.commit()

async def seed_default_questions(conn: aiosqlite.Connection, guild_id: int):
    for category, questions in DEFAULT_QUESTIONS.items():
        cur = await conn.execute("SELECT 1 FROM categories WHERE guild_id = ? AND name = ? LIMIT 1", (guild_id, category))
        exists = await cur.fetchone()
        if exists:
            continue
        await conn.execute("INSERT INTO categories (guild_id, name) VALUES (?, ?)", (guild_id, category))
        ts = int(time.time())
        for q in questions:
            await conn.execute(
                "INSERT INTO questions (guild_id, category, author_id, content, created_at) VALUES (?, ?, ?, ?, ?)",
                (guild_id, category, 0, q, ts)
            )
    await conn.commit()

# DB helpers (use bot.db)
async def add_category(guild_id: int, name: str):
    await bot.db.execute("INSERT OR IGNORE INTO categories (guild_id, name) VALUES (?, ?)", (guild_id, name))
    await bot.db.commit()

async def add_question(guild_id: int, category: str, author_id: int, content: str, ts: int):
    await bot.db.execute(
        "INSERT INTO questions (guild_id, category, author_id, content, created_at) VALUES (?, ?, ?, ?, ?)",
        (guild_id, category, author_id, content, ts),
    )
    await bot.db.commit()

async def get_questions(guild_id: int, category: str):
    bot.db.row_factory = aiosqlite.Row
    cur = await bot.db.execute("SELECT content FROM questions WHERE guild_id = ? AND category = ?", (guild_id, category))
    rows = await cur.fetchall()
    return [r["content"] for r in rows]

async def get_categories(guild_id: int):
    bot.db.row_factory = aiosqlite.Row
    cur = await bot.db.execute("SELECT name FROM categories WHERE guild_id = ?", (guild_id,))
    rows = await cur.fetchall()
    return [r["name"] for r in rows]

# Channel resolver (string-based)
CHANNEL_MENTION_RE = re.compile(r"<#(\d+)>")
async def resolve_text_channel_by_string(guild: Optional[discord.Guild], raw: str) -> Optional[discord.TextChannel]:
    if not guild or not raw:
        return None
    raw = raw.strip()
    m = CHANNEL_MENTION_RE.match(raw)
    if m:
        try:
            cid = int(m.group(1)); ch = guild.get_channel(cid)
            return ch if isinstance(ch, discord.TextChannel) else None
        except Exception:
            return None
    if raw.isdigit():
        try:
            ch = guild.get_channel(int(raw)); return ch if isinstance(ch, discord.TextChannel) else None
        except Exception:
            return None
    for ch in guild.text_channels:
        if ch.name.lower() == raw.lower(): return ch
    raw_l = raw.lower()
    for ch in guild.text_channels:
        if raw_l in ch.name.lower(): return ch
    return None

# Background revive loop
async def check_inactivity_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            bot.db.row_factory = aiosqlite.Row
            cur = await bot.db.execute("SELECT * FROM revive_channels")
            rows = await cur.fetchall()
            now_ts = int(time.time())
            for row in rows:
                try:
                    if now_ts - row["last_message_ts"] >= row["inactivity_threshold"]:
                        channel = bot.get_channel(row["channel_id"])
                        if channel and isinstance(channel, discord.TextChannel):
                            qs = await get_questions(row["guild_id"], row["category"])
                            if qs:
                                q = random.choice(qs)
                                try:
                                    await channel.send(f"💡 {q}")
                                except Exception:
                                    logger.exception("Failed to send to channel %s", row["channel_id"])
                                await bot.db.execute("UPDATE revive_channels SET last_message_ts = ? WHERE id = ?", (now_ts, row["id"]))
                                await bot.db.commit()
                except Exception:
                    logger.exception("Failed to process revive row id=%s", row["id"])
        except Exception:
            logger.exception("Error in inactivity loop")
        await asyncio.sleep(60)

# Simple commands (examples)
@tree.command(name="ping", description="Test if bot responds")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="add_category", description="Add a new question category")
@app_commands.default_permissions(manage_guild=True)
async def add_category_cmd(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        await add_category(interaction.guild_id, name)
        await interaction.followup.send(f"✅ Category '{name}' added.", ephemeral=True)
    except Exception:
        logger.exception("add_category failed"); await interaction.followup.send("❌ Failed to add category.", ephemeral=True)

# Startup and sync
@bot.event
async def on_ready():
    logger.info("Bot ready: %s", bot.user)
    # ensure DB and seed for guilds bot is in
    await init_db(bot.db)
    for g in bot.guilds:
        try:
            await seed_default_questions(bot.db, g.id)
        except Exception:
            logger.exception("Seeding failed for guild %s", g.id)
    # sync commands (global then per-guild fallback)
    try:
        await tree.sync(); logger.info("Commands synced globally.")
    except Exception:
        logger.exception("Global sync failed, trying per-guild")
        for g in bot.guilds:
            try:
                await tree.sync(guild=g); logger.info("Synced for guild %s", g.id)
            except Exception:
                logger.exception("Failed to sync for guild %s", g.id)

async def main():
    if not TOKEN:
        logger.error("No token provided. Set DISCORD_BOT_TOKEN or TOKEN env var."); return
    bot.db = await aiosqlite.connect(DB_PATH)
    bot.db.row_factory = aiosqlite.Row
    await init_db(bot.db)
    # start background task
    bot.loop.create_task(check_inactivity_loop())
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
