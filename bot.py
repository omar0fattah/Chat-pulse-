# bot.py
import os
import re
import time
import random
import logging
import asyncio
import aiosqlite
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

# ---------------- CONFIG ----------------
TOKEN = os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("TOKEN")
DB_PATH = os.environ.get("DB_PATH", "chatpulse.db")
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("chatpulse")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ---------------- DEFAULT QUESTIONS (small sample, extend as needed) ----------------
DEFAULT_QUESTIONS = {
    "general": [
        "If you could have dinner with any fictional character, who?",
        "What's the weirdest food combination you enjoy?",
        "If you woke up with a superpower tomorrow, what would it be?"
    ],
    "minecraft": [
        "Wooden sword or stone pickaxe first?",
        "What's your go-to biome to build in?"
    ],
    "apex": [
        "Who's your main in Apex and why?",
        "Hot take: Which legend is overrated?"
    ]
}

# ---------------- DB SCHEMA ----------------
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

# ---------------- DB HELPERS (use single persistent connection: bot.db) ----------------
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

async def add_revive_channel(guild_id: int, channel_id: int, category: str, threshold: int):
    await bot.db.execute(
        "INSERT INTO revive_channels (guild_id, channel_id, category, inactivity_threshold, last_message_ts) VALUES (?, ?, ?, ?, ?)",
        (guild_id, channel_id, category, threshold, int(time.time())),
    )
    await bot.db.commit()

async def remove_revive_channel(guild_id: int, channel_id: int):
    await bot.db.execute("DELETE FROM revive_channels WHERE guild_id = ? AND channel_id = ?", (guild_id, channel_id))
    await bot.db.commit()

async def get_revive_channels(guild_id: int):
    bot.db.row_factory = aiosqlite.Row
    cur = await bot.db.execute("SELECT * FROM revive_channels WHERE guild_id = ?", (guild_id,))
    rows = await cur.fetchall()
    return [dict(r) for r in rows]

# ---------------- AUTOCOMPLETE ----------------
async def category_autocomplete(interaction: discord.Interaction, current: str):
    if interaction.guild_id is None:
        return []
    names = await get_categories(interaction.guild_id)
    return [app_commands.Choice(name=name, value=name) for name in names if current.lower() in name.lower()]

# ---------------- CHANNEL RESOLUTION ----------------
CHANNEL_MENTION_RE = re.compile(r"<#(\d+)>")

async def resolve_text_channel_by_string(guild: Optional[discord.Guild], raw: str) -> Optional[discord.TextChannel]:
    if not guild or not raw:
        return None
    raw = raw.strip()
    m = CHANNEL_MENTION_RE.match(raw)
    if m:
        try:
            cid = int(m.group(1))
            ch = guild.get_channel(cid)
            return ch if isinstance(ch, discord.TextChannel) else None
        except Exception:
            return None
    if raw.isdigit():
        try:
            ch = guild.get_channel(int(raw))
            return ch if isinstance(ch, discord.TextChannel) else None
        except Exception:
            return None
    for ch in guild.text_channels:
        if ch.name.lower() == raw.lower():
            return ch
    raw_l = raw.lower()
    for ch in guild.text_channels:
        if raw_l in ch.name.lower():
            return ch
    return None

# ---------------- BACKGROUND LOOP ----------------
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
                    # row is a mapping
                    last_ts = row["last_message_ts"] or 0
                    threshold = row["inactivity_threshold"] or 0
                    if now_ts - last_ts >= threshold:
                        channel = bot.get_channel(row["channel_id"])
                        if channel and isinstance(channel, discord.TextChannel):
                            qs = await get_questions(row["guild_id"], row["category"])
                            if qs:
                                q = random.choice(qs)
                                try:
                                    await channel.send(f"💡 {q}")
                                except Exception:
                                    logger.exception("Failed to send revive message to channel %s", row["channel_id"])
                                await bot.db.execute("UPDATE revive_channels SET last_message_ts = ? WHERE id = ?", (now_ts, row["id"]))
                                await bot.db.commit()
                except Exception:
                    # use mapping access for id
                    try:
                        rid = row["id"]
                    except Exception:
                        rid = "<unknown>"
                    logger.exception("Failed to process revive row id=%s", rid)
        except Exception:
            logger.exception("Error in inactivity loop")
        await asyncio.sleep(60)

# ---------------- SLASH COMMANDS ----------------
@tree.command(name="help", description="Show all available commands and what they do")
async def help_cmd(interaction: discord.Interaction):
    help_text = (
        "📖 **ChatPulse Bot Commands**\n\n"
        "🔹 `/ping` — Test if the bot responds.\n"
        "🔹 `/add_category <name>` — Add a new question category. (Admins only)\n"
        "🔹 `/add_question <category> <content>` — Add a question to a category. (Admins only)\n"
        "🔹 `/list_questions <category>` — List questions in a category.\n"
        "🔹 `/setup_revive <channel> <category> <threshold_seconds>` — Configure revive using a typed channel. (Admins only)\n"
        "🔹 `/remove_revive <channel>` — Remove revive for a channel. (Admins only)\n"
        "🔹 `/revive_now <channel>` — Trigger a manual revive. (Admins only)\n"
        "🔹 `/reset_categories` — Re-add default categories/questions for this server. (Admins only)\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@tree.command(name="ping", description="Test if bot responds")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="add_category", description="Add a new question category")
@app_commands.default_permissions(manage_guild=True)
async def add_category_cmd(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild_id is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        await add_category(interaction.guild_id, name)
        await interaction.followup.send(f"✅ Category '{name}' added.", ephemeral=True)
    except Exception:
        logger.exception("add_category failed")
        await interaction.followup.send("❌ Failed to add category.", ephemeral=True)

@tree.command(name="add_question", description="Add a question to a category")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def add_question_cmd(interaction: discord.Interaction, category: str, content: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild_id is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        cats = await get_categories(interaction.guild_id)
        if category not in cats:
            await interaction.followup.send(f"⚠️ Category '{category}' not found. Add it with /add_category or run /reset_categories.", ephemeral=True)
            return
        await add_question(interaction.guild_id, category, interaction.user.id, content, int(time.time()))
        await interaction.followup.send(f"✅ Question added to '{category}'.", ephemeral=True)
    except Exception:
        logger.exception("add_question failed")
        await interaction.followup.send("❌ Failed to add question.", ephemeral=True)

@tree.command(name="list_questions", description="List questions in a category")
@app_commands.autocomplete(category=category_autocomplete)
async def list_questions_cmd(interaction: discord.Interaction, category: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild_id is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        qs = await get_questions(interaction.guild_id, category)
        if not qs:
            await interaction.followup.send("No questions found.", ephemeral=True)
            return
        # limit to 50 items to avoid huge messages
        await interaction.followup.send("\n".join([f"- {q}" for q in qs[:50]]), ephemeral=True)
    except Exception:
        logger.exception("list_questions failed")
        await interaction.followup.send("❌ Failed to list questions.", ephemeral=True)

@tree.command(name="reset_categories", description="Reseed default categories/questions for this server")
@app_commands.default_permissions(manage_guild=True)
async def reset_categories(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild_id is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        await seed_default_questions(bot.db, interaction.guild_id)
        await interaction.followup.send("✅ Default categories and questions re-added (if missing).", ephemeral=True)
    except Exception:
        logger.exception("reset_categories failed")
        await interaction.followup.send("❌ Failed to reset categories.", ephemeral=True)

@tree.command(name="setup_revive", description="Configure revive for a channel (typed channel mention/ID/name)")
@app_commands.default_permissions(manage_guild=True)
async def setup_revive(interaction: discord.Interaction, channel: str, category: str, threshold_seconds: int):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        ch = await resolve_text_channel_by_string(interaction.guild, channel)
        if not ch:
            await interaction.followup.send("⚠️ Could not resolve that channel. Use a mention, ID, or name.", ephemeral=True); return
        cats = await get_categories(interaction.guild_id)
        if category not in cats:
            await interaction.followup.send(f"⚠️ Category '{category}' not found.", ephemeral=True); return
        if threshold_seconds <= 0:
            await interaction.followup.send("⚠️ Threshold must be a positive number of seconds.", ephemeral=True); return
        await add_revive_channel(interaction.guild_id, ch.id, category, threshold_seconds)
        await interaction.followup.send(f"✅ Revive configured for {ch.mention} (category: {category}, threshold: {threshold_seconds}s).", ephemeral=True)
    except Exception:
        logger.exception("setup_revive failed")
        await interaction.followup.send("❌ Failed to setup revive.", ephemeral=True)

@tree.command(name="remove_revive", description="Remove revive for a typed channel")
@app_commands.default_permissions(manage_guild=True)
async def remove_revive(interaction: discord.Interaction, channel: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        ch = await resolve_text_channel_by_string(interaction.guild, channel)
        if not ch:
            await interaction.followup.send("⚠️ Could not resolve that channel.", ephemeral=True); return
        await remove_revive_channel(interaction.guild_id, ch.id)
        await interaction.followup.send(f"✅ Revive removed for {ch.mention}.", ephemeral=True)
    except Exception:
        logger.exception("remove_revive failed")
        await interaction.followup.send("❌ Failed to remove revive.", ephemeral=True)

@tree.command(name="revive_now", description="Trigger a manual revive for a typed channel")
@app_commands.default_permissions(manage_guild=True)
async def revive_now(interaction: discord.Interaction, channel: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.guild is None:
        await interaction.followup.send("This command must be used in a server.", ephemeral=True); return
    try:
        ch = await resolve_text_channel_by_string(interaction.guild, channel)
        if not ch:
            await interaction.followup.send("⚠️ Could not resolve that channel.", ephemeral=True); return
        # pick a random question from any category configured for that channel (if present)
        async with bot.db.execute("SELECT category FROM revive_channels WHERE guild_id = ? AND channel_id = ? LIMIT 1", (interaction.guild_id, ch.id)) as cur:
            row = await cur.fetchone()
        if not row:
            await interaction.followup.send("⚠️ That channel is not configured for revive.", ephemeral=True); return
        qs = await get_questions(interaction.guild_id, row["category"])
        if not qs:
            await interaction.followup.send("⚠️ No questions in that category.", ephemeral=True); return
        q = random.choice(qs)
        try:
            await ch.send(f"💡 {q}")
        except Exception:
            logger.exception("Failed to send manual revive to %s", ch.id)
            await interaction.followup.send("❌ Failed to send message to channel (missing permissions?).", ephemeral=True); return
        await bot.db.execute("UPDATE revive_channels SET last_message_ts = ? WHERE guild_id = ? AND channel_id = ?", (int(time.time()), interaction.guild_id, ch.id))
        await bot.db.commit()
        await interaction.followup.send(f"✅ Sent revive to {ch.mention}.", ephemeral=True)
    except Exception:
        logger.exception("revive_now failed")
        await interaction.followup.send("❌ Failed to revive now.", ephemeral=True)

# ---------------- STARTUP / SYNC ----------------
@bot.event
async def on_ready():
    logger.info("Bot ready: %s (id=%s)", bot.user, bot.user.id)
    # seed defaults for guilds the bot is in
    try:
        await init_db(bot.db)
    except Exception:
        logger.exception("init_db failed on_ready")
    for g in bot.guilds:
        try:
            await seed_default_questions(bot.db, g.id)
        except Exception:
            logger.exception("Seeding failed for guild %s", g.id)
    # sync commands (global then per-guild fallback)
    try:
        await tree.sync()
        logger.info("Commands synced globally.")
    except Exception:
        logger.exception("Global sync failed, trying per-guild")
        for g in bot.guilds:
            try:
                await tree.sync(guild=g)
                logger.info("Synced commands for guild %s", g.id)
            except Exception:
                logger.exception("Failed to sync for guild %s", g.id)

async def main():
    if not TOKEN:
        logger.error("No token provided. Set DISCORD_BOT_TOKEN or TOKEN environment variable.")
        return
    # open a single persistent DB connection and attach to bot
    bot.db = await aiosqlite.connect(DB_PATH)
    bot.db.row_factory = aiosqlite.Row
    await init_db(bot.db)
    # schedule background loop on the current running loop (do NOT access bot.loop)
    asyncio.create_task(check_inactivity_loop())
    # start the bot (this will block until disconnect)
    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down (KeyboardInterrupt)")
    except Exception:
        logger.exception("Fatal error in main")
