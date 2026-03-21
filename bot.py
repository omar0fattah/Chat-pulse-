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
        
"Who's your main in Apex and why?",
"Hot take: Which legend is overrated?",
"What's the dumbest way you've died in Apex?",
"Which map do you love/hate the most?",
"Best weapon combo for ranked?",
"Do you prefer solo queue or squads?",
"Which legend needs a buff right now?",
"What’s your favorite ultimate ability?",
"Which legend do you think is hardest to master?",
"Best skin you own?",
"Which heirloom is the coolest?",
"What’s your go-to drop spot?",
"Do you prefer aggressive or passive playstyle?",
"Which gun feels underrated?",
"What’s the most clutch play you’ve ever made?",
"Which legend do you ban from your squad?",
"Best legend for beginners?",
"Which gun do you craft every time?",
"What’s your favorite limited-time mode?",
"Which legend voice lines crack you up?",
"Best duo combo?",
"Which map rotation do you hate?",
"What’s your favorite finisher animation?",
"Which gun do you never pick up?",
"Best sniper in the game?",
"Which legend is most annoying to fight?",
"What’s your favorite event?",
"Which legend has the best lore?",
"Best legend for clutching 1v3?",
"Which gun feels broken?",
"What’s your favorite ranked split?",
"Which legend do you think is most toxic?",
"Best gun for close range?",
"Which legend ult saves you most?",
"What’s your favorite battle pass reward?",
"Which legend do you main in arenas?",
"Best gun for arenas?",
"Which legend combo dominates ranked?",
"What’s your favorite meme about Apex?",
"Which gun feels most satisfying to use?",
"Best legend for movement?",
"Which legend ult is most useless?",
"What’s your favorite Apex season?",
"Which gun do you craft instantly?",
"Best legend for solo queue?",
"Which gun do you think needs a nerf?",
"What’s your favorite Apex trailer?",
"Which legend do you think is most stylish?",
"Best gun for mid-range fights?",
"Which legend ult is most fun?",
"What’s your favorite Apex crossover?",
"Which gun do you think is most balanced?",
"Best legend for team play?",
"Which gun do you think is most OP?",
"What’s your favorite Apex meme?",
"Which legend ult is most annoying?",
"Best gun for hipfire?",
"Which legend ult is most clutch?",
"What’s your favorite Apex event skin?",
"Which gun do you think is most fun?",
"Best legend for ranked grind?",
"Which gun do you think is most hated?",
"What’s your favorite Apex emote?",
"Which legend ult is most broken?",
"Best gun for spray control?",
"Which legend ult is most tactical?",
"What’s your favorite Apex lore moment?",
"Which gun do you think is most iconic?",
"Best legend for pubs?",
"Which gun do you think is most underrated?",
"What’s your favorite Apex finisher?",
"Which legend ult is most stylish?",
"Best gun for long range?",
"Which legend ult is most feared?",
"What’s your favorite Apex heirloom?",
"Which gun do you think is most fun to master?",
"Best legend for clutch plays?",
"Which gun do you think is most satisfying?",
"What’s your favorite Apex map?",
"Which legend ult is most troll?",
"Best gun for ranked?",
"Which legend ult is most hype?",
"What’s your favorite Apex squad comp?",
"Which gun do you think is most skillful?",
"Best legend for aggressive play?",
"Which gun do you think is most versatile?",
"What’s your favorite Apex ranked memory?",
"Which legend ult is most game-changing?",
"Best gun for casual play?",
"Which legend ult is most tactical?",
"What’s your favorite Apex cosmetic?",
"Which gun do you think is most reliable?",
"Best legend for defense?",
"Which gun do you think is most fun in pubs?",
"What’s your favorite Apex clutch?",
"Which legend ult is most hype to use?",
"Best gun for arenas ranked?",
"Which legend ult is most troll-worthy?",
"What’s your favorite Apex squad meme?",
"Which gun do you think is most fun in ranked?",
"Best legend for late game?",
"Which gun do you think is most fun overall?",
"What’s your favorite Apex season theme?",
"Which legend ult is most satisfying?",
"Best gun for competitive play?",
"Which legend ult is most hype in tournaments?",
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
@tree.command(name="help", description="Show all available commands and what they do")
async def help_cmd(interaction: discord.Interaction):
    help_text = """
📖 **ChatPulse Bot Commands**

🔹 `/ping` — Test if the bot responds.
🔹 `/add_category <name>` — Add a new question category. (Admins only)
🔹 `/add_question <category> <content>` — Add a question to a category. (Admins only)
🔹 `/delete_question <category> <content>` — Delete a question from a category. (Admins only)
🔹 `/list_questions <category>` — List up to 10 questions in a category.
🔹 `/setup_revive <channel> <category> <hours>` — Configure revive logic for a channel. (Admins only)
🔹 `/remove_revive <channel>` — Remove revive logic from a channel. (Admins only)
🔹 `/revive_now <channel> [category]` — Trigger a manual revive message. (Admins only)
🔹 `/status` — Show revive channel status and thresholds.
🔹 `/help` — Show this help message.
"""
    await interaction.response.send_message(help_text, ephemeral=True)


@tree.command(name="ping", description="Test if bot responds")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="add_category", description="Add a new question category")
@app_commands.default_permissions(manage_guild=True)
async def add_category_cmd(interaction: discord.Interaction, name: str):
    await add_category(interaction.guild_id, name)
    await interaction.response.send_message(f"✅ Category '{name}' added.", ephemeral=True)

@tree.command(name="add_question", description="Add a question to a category")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def add_question_cmd(interaction: discord.Interaction, category: str, content: str):
    await add_question(interaction.guild_id, category, interaction.user.id, content, int(asyncio.get_event_loop().time()))
    await interaction.response.send_message(f"✅ Question added to '{category}'.", ephemeral=True)

@tree.command(name="delete_question", description="Delete a question from a category")
@app_commands.default_permissions(manage_guild=True)  # Only admins/mods can delete
@app_commands.autocomplete(category=category_autocomplete)
async def delete_question_cmd(interaction: discord.Interaction, category: str, content: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM questions WHERE guild_id = ? AND category = ? AND content = ?",
            (interaction.guild_id, category, content)
        )
        # 👇 This is the check you add
        if cur.rowcount == 0:
            await interaction.response.send_message(
                f"⚠️ No matching question found in '{category}'.",
                ephemeral=True
            )
            return
        await db.commit()

    await interaction.response.send_message(
        f"❌ Question '{content}' deleted from '{category}'.",
        ephemeral=True
    )


@tree.command(name="list_questions", description="List questions in a category")
@app_commands.autocomplete(category=category_autocomplete)
async def list_questions_cmd(interaction: discord.Interaction, category: str):
    qs = await get_questions(interaction.guild_id, category)
    if not qs:
        await interaction.response.send_message("No questions found.", ephemeral=True)
    else:
        await interaction.response.send_message("\n".join([f"- {q}" for q in qs[:10]]), ephemeral=True)

@tree.command(name="setup_revive", description="Set up revive for a channel")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel, category: str, hours: int):
    threshold = hours * 3600
    await add_revive_channel(interaction.guild_id, channel.id, category, threshold)
    await interaction.response.send_message(
        f"✅ Revive set for {channel.mention} with category '{category}' after {hours} hours of inactivity.",
        ephemeral=True
    )

@tree.command(name="remove_revive", description="Remove revive from a channel")
@app_commands.default_permissions(manage_guild=True)
async def remove_revive_cmd(interaction: discord.Interaction, channel: discord.TextChannel):
    await remove_revive_channel(interaction.guild_id, channel.id)
    await interaction.response.send_message(f"❌ Revive removed from {channel.mention}.", ephemeral=True)

@tree.command(name="revive_now", description="Trigger a manual revive")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def revive_now(interaction: discord.Interaction, channel: discord.TextChannel, category: str = "general"):
    qs = await get_questions(interaction.guild_id, category)
    if qs:
        q = random.choice(qs)
        await channel.send(f"💡 {q}")
        await interaction.response.send_message("✅ Revive message sent.", ephemeral=True)
    else:
        await interaction.response.send_message(f"No questions available in '{category}'.", ephemeral=True)

@tree.command(name="status", description="Show bot status")
async def status(interaction: discord.Interaction):
    channels = await get_revive_channels(interaction.guild_id)
    if not channels:
        await interaction.response.send_message("No revive channels configured.", ephemeral=True)
    else:
        lines = []
        for ch in channels:
            channel = interaction.guild.get_channel(ch["channel_id"])
            lines.append(
                f"{channel.mention} → Category: {ch['category']}, Threshold: {ch['inactivity_threshold']//3600}h"
            )
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    await init_db()
    for guild in bot.guilds:
        await seed_default_questions(guild.id)
    bot.loop.create_task(check_inactivity_loop(bot))
    await tree.sync()
    print(f"Bot ready: {bot.user}")

# ==================== RUN ====================
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ No bot token found in environment variables.")

