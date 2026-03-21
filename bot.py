import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiosqlite
import random

# ==================== CONFIG ====================
TOKEN = os.environ.get('TOKEN') or os.environ.get('DISCORD_BOT_TOKEN')
DB_PATH = 'chatpulse.db'

# ==================== BOT SETUP ====================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ==================== DEFAULT QUESTIONS ====================
DEFAULT_QUESTIONS = {
    "apex": [
        "Who's your main in Apex and why?",
        "Hot take: Which legend is overrated?",
        "What's the dumbest way you've died in Apex?",
    ],
    "minecraft": [
        "Wooden sword or stone pickaxe first?",
        "What's your go-to biome to build in?",
        "Creeper or skeleton - which is more annoying?",
    ],
    "cod": [
        "Favorite COD game of all time?",
        "SMG or Assault Rifle?",
        "Hardpoint or Search & Destroy?",
    ],
    "general": [
        "If you could have dinner with any fictional character, who?",
        "What's the weirdest food combination you enjoy?",
        "If you woke up with a superpower tomorrow, what would it be?",
    ]
}

# ==================== DATABASE ====================
_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    name TEXT NOT NULL
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

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(_SCHEMA_SQL)
        await db.commit()

async def seed_default_questions(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        for category, questions in DEFAULT_QUESTIONS.items():
            await db.execute("INSERT OR IGNORE INTO categories (guild_id, name) VALUES (?, ?)", (guild_id, category))
            for q in questions:
                await db.execute(
                    "INSERT INTO questions (guild_id, category, author_id, content, created_at) VALUES (?, ?, ?, ?, ?)",
                    (guild_id, category, 0, q, int(asyncio.get_event_loop().time()))
                )
        await db.commit()

# ==================== HELPERS ====================
async def add_category(guild_id: int, name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO categories (guild_id, name) VALUES (?, ?)", (guild_id, name))
        await db.commit()

async def add_question(guild_id: int, category: str, author_id: int, content: str, ts: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO questions (guild_id, category, author_id, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (guild_id, category, author_id, content, ts),
        )
        await db.commit()

async def get_questions(guild_id: int, category: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT content FROM questions WHERE guild_id = ? AND category = ?", (guild_id, category))
        rows = await cur.fetchall()
        return [r["content"] for r in rows]

async def add_revive_channel(guild_id: int, channel_id: int, category: str, threshold: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO revive_channels (guild_id, channel_id, category, inactivity_threshold, last_message_ts) VALUES (?, ?, ?, ?, ?)",
            (guild_id, channel_id, category, threshold, int(asyncio.get_event_loop().time())),
        )
        await db.commit()

async def remove_revive_channel(guild_id: int, channel_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM revive_channels WHERE guild_id = ? AND channel_id = ?", (guild_id, channel_id))
        await db.commit()

async def get_revive_channels(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM revive_channels WHERE guild_id = ?", (guild_id,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

# ==================== CATEGORY HELPER ====================
async def get_categories(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT name FROM categories WHERE guild_id = ?", (guild_id,))
        rows = await cur.fetchall()
        return [r["name"] for r in rows]

async def category_autocomplete(interaction: discord.Interaction, current: str):
    names = await get_categories(interaction.guild_id)
    return [
        app_commands.Choice(name=name, value=name)
        for name in names if current.lower() in name.lower()
    ]

# ==================== BACKGROUND LOOP ====================
async def check_inactivity_loop(bot: commands.Bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM revive_channels")
            rows = await cur.fetchall()
        now_ts = int(asyncio.get_event_loop().time())
        for row in rows:
            if now_ts - row["last_message_ts"] >= row["inactivity_threshold"]:
                channel = bot.get_channel(row["channel_id"])
                if channel:
                    questions = await get_questions(row["guild_id"], row["category"])
                    if questions:
                        q = random.choice(questions)
                        try:
                            await channel.send(f"💡 {q}")
                            async with aiosqlite.connect(DB_PATH) as db:
                                await db.execute(
                                    "UPDATE revive_channels SET last_message_ts = ? WHERE id = ?",
                                    (now_ts, row["id"]),
                                )
                                await db.commit()
                        except Exception as e:
                            print(f"Failed to send revive: {e}")
        await asyncio.sleep(60)

# ==================== SLASH COMMANDS ====================
@tree.command(name="ping", description="Test if bot responds")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="add_category", description="Add a new question category")
async def add_category_cmd(interaction: discord.Interaction, name: str):
    await add_category(interaction.guild_id, name)
    await interaction.response.send_message(f"✅ Category '{name}' added.", ephemeral=True)

@tree.command(name="add_question", description="Add a question to a category")
@app_commands.autocomplete(category=category_autocomplete)
async def add_question_cmd(interaction: discord.Interaction, category: str, content: str):
    await add_question(interaction.guild_id, category, interaction.user.id, content, int(asyncio.get_event_loop().time()))
    await interaction.response.send_message(f"✅ Question added to '{category}'.", ephemeral=True)

@tree.command(name="list_questions", description="List questions in a category")
@app_commands.autocomplete(category=category_autocomplete)
async def list_questions_cmd(interaction: discord.Interaction, category: str):
    qs = await get_questions(interaction.guild_id, category)
    if not qs:
        await interaction.response.send_message("No questions found.", ephemeral=True)
    else:
        await interaction.response.send_message("\n".join([f"- {q}" for q in qs[:10]]), ephemeral=True)

@tree.command(name="setup_revive", description="Set up revive for a channel")
@app_commands.autocomplete(category=category_autocomplete)
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel, category: str, hours: int):
    threshold = hours * 3600
    await add_revive_channel(interaction.guild_id, channel.id, category, threshold)
    await interaction.response.send_message(
        f"✅ Revive set for {channel.mention} with category '{category}' after {hours} hours of inactivity.",
        ephemeral=True
    )

@tree.command(name="remove_revive", description="Remove revive from a channel")
async def remove_revive_cmd(interaction: discord.Interaction, channel: discord.TextChannel):
    await remove_revive_channel(interaction.guild_id, channel.id)
    await interaction.response.send_message(f"❌ Revive removed from {channel.mention}.", ephemeral=True)

@
