# chatpulse_full.py
# Full ChatPulse bot — complete, ready-to-paste, includes:
# - All default questions (apex, minecraft, cod, general)
# - All useful commands (ping, help, add_category, add_question, delete_question,
#   list_questions, setup_revive, remove_revive, revive_now, status, reset_categories, debug_categories)
# - Robust channel resolution (picker + typed input)
# - Interaction deferral to avoid timeouts
# - Global command sync
# - DB seeding without duplicates
# - Background inactivity loop
# - Defensive logging and error handling
#
# Requirements: discord.py (2.x), aiosqlite
# Set environment variable DISCORD_BOT_TOKEN (or TOKEN) before running.

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

# ==================== CONFIG ====================
TOKEN = os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("TOKEN") or "YOUR_TOKEN"
DB_PATH = os.environ.get("DB_PATH", "chatpulse.db")
LOG_LEVEL = logging.INFO

# ==================== LOGGING ====================
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("chatpulse")

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
        "Which legend ult is most hype in tournaments?"
    ],
    "minecraft": [
        "Wooden sword or stone pickaxe first?",
        "What's your go-to biome to build in?",
        "Creeper or skeleton - which is more annoying?",
        "What’s your favorite block to build with?",
        "Best food source early game?",
        "Do you prefer survival or creative?",
        "What’s your favorite mob?",
        "Nether or End — which is scarier?",
        "Best enchantment combo for tools?",
        "What’s your favorite redstone contraption?",
        "Do you prefer singleplayer or multiplayer?",
        "Best armor enchantments?",
        "What’s your favorite Minecraft update?",
        "Do you use shields often?",
        "Best biome for resources?",
        "What’s your favorite hostile mob?",
        "Do you prefer farming or mining?",
        "Best potion effect?",
        "What’s your favorite Minecraft boss?",
        "Do you prefer villages or strongholds?",
        "Best building style?",
        "What’s your favorite Minecraft soundtrack?",
        "Do you prefer caves or mountains?",
        "Best weapon enchantments?",
        "What’s your favorite Minecraft animal?",
        "Do you prefer exploring or building?",
        "Best Nether resource?",
        "What’s your favorite Minecraft dimension?",
        "Do you prefer boats or minecarts?",
        "Best XP farm design?",
        "What’s your favorite Minecraft biome?",
        "Do you prefer fishing or hunting?",
        "Best enchantment for bows?",
        "What’s your favorite Minecraft structure?",
        "Do you prefer trading or crafting?",
        "Best enchantment for swords?",
        "What’s your favorite Minecraft block?",
        "Do you prefer snow or desert biomes?",
        "Best enchantment for pickaxes?",
        "What’s your favorite Minecraft mob drop?",
        "Do you prefer exploring caves or oceans?",
        "Best enchantment for armor?",
        "What’s your favorite Minecraft village profession?",
        "Do you prefer farming crops or animals?",
        "Best enchantment for tridents?",
        "What’s your favorite Minecraft adventure?",
        "Do you prefer building houses or castles?",
        "Best enchantment for crossbows?",
        "What’s your favorite Minecraft mini-game?",
        "Do you prefer survival challenges or creative builds?",
        "Best enchantment for axes?",
        "What’s your favorite Minecraft biome feature?",
        "Do you prefer Nether fortresses or Bastions?",
        "Best enchantment for Elytra?",
        "What’s your favorite Minecraft cave generation?",
        "Do you prefer jungle or swamp biomes?",
        "Best enchantment for hoes?",
        "What’s your favorite Minecraft villager trade?",
        "Do you prefer plains or taiga biomes?",
        "Best enchantment for fishing rods?",
        "What’s your favorite Minecraft dungeon?",
        "Do you prefer ocean monuments or woodland mansions?",
        "Best enchantment for shovels?",
        "What’s your favorite Minecraft rare item?",
        "Do you prefer lava lakes or ice spikes?",
        "Best enchantment for helmets?",
        "What’s your favorite Minecraft biome decoration?",
        "Do you prefer flower forests or mushroom islands?",
        "Best enchantment for boots?",
        "What’s your favorite Minecraft cave mob?",
        "Do you prefer desert temples or jungle temples?",
        "Best enchantment for chestplates?",
        "What’s your favorite Minecraft rare mob?",
        "Do you prefer pillager outposts or igloos?",
        "Best enchantment for leggings?",
        "What’s your favorite Minecraft cave loot?",
        "Do you prefer abandoned mineshafts or strongholds?",
        "Best enchantment for shields?",
        "What’s your favorite Minecraft rare structure?",
        "Do you prefer coral reefs or kelp forests?",
        "Best enchantment for tools overall?",
        "What’s your favorite Minecraft rare biome?",
        "Do you prefer mesa or savanna biomes?",
        "Best enchantment for weapons overall?",
        "What’s your favorite Minecraft rare block?",
        "Do you prefer quartz or obsidian builds?",
        "Best enchantment for armor overall?",
        "What’s your favorite Minecraft rare enchantment?",
        "Do you prefer enchanted books or anvils?",
        "Best enchantment for utility?",
        "What’s your favorite Minecraft rare potion?",
        "Do you prefer brewing or enchanting?",
        "Best enchantment for combat?",
        "What’s your favorite Minecraft rare chest loot?",
        "Do you prefer treasure maps or exploration?",
        "Best enchantment for exploration?",
        "What’s your favorite Minecraft rare seed?",
        "Do you prefer speedrunning or casual play?",
        "Best enchantment for farming?",
        "What’s your favorite Minecraft rare glitch?",
        "Do you prefer mods or vanilla?",
        "Best enchantment for building?",
        "What’s your favorite Minecraft rare update?",
        "Do you prefer snapshots or full releases?",
        "Best enchantment for mining?",
        "What’s your favorite Minecraft rare achievement?",
        "Do you prefer hardcore or peaceful?"
    ],
    "cod": [
        "Favorite COD game of all time?",
        "SMG or Assault Rifle?",
        "Hardpoint or Search & Destroy?",
        "Which COD campaign had the best story?",
        "Best multiplayer map ever?",
        "Do you prefer Zombies or Campaign?",
        "Which COD had the best soundtrack?",
        "Best sniper rifle across all CODs?",
        "Which COD had the most balanced multiplayer?",
        "Favorite killstreak reward?",
        "Which COD had the best graphics?",
        "Best COD protagonist?",
        "Which COD villain was most memorable?",
        "Best COD Zombies map?",
        "Which COD had the best DLC?",
        "Favorite COD weapon class?",
        "Which COD had the best multiplayer progression?",
        "Best COD perk?",
        "Which COD had the most toxic lobbies?",
        "Favorite COD esports moment?",
        "Which COD had the best customization?",
        "Best COD secondary weapon?",
        "Which COD had the best co-op mode?",
        "Favorite COD mission?",
        "Which COD had the best gunplay?",
        "Best COD shotgun?",
        "Which COD had the best battle pass?",
        "Favorite COD operator?",
        "Which COD had the best campaign twist?",
        "Best COD pistol?",
        "Which COD had the best Zombies Easter eggs?",
        "Favorite COD multiplayer mode?",
        "Which COD had the best launch maps?",
        "Best COD SMG?",
        "Which COD had the best sniper mechanics?",
        "Favorite COD killstreak?",
        "Which COD had the best community?",
        "Best COD assault rifle?",
        "Which COD had the best Zombies boss?",
        "Favorite COD multiplayer weapon?",
        "Which COD had the best campaign ending?",
        "Best COD LMG?",
        "Which COD had the best prestige system?",
        "Favorite COD multiplayer map?",
        "Which COD had the best gun sounds?",
        "Best COD tactical equipment?",
        "Which COD had the best Zombies story?",
        "Favorite COD multiplayer class setup?",
        "Which COD had the best campaign characters?",
        "Best COD lethal equipment?",
        "Which COD had the best multiplayer balance?",
        "Favorite COD multiplayer killstreak?",
        "Which COD had the best Zombies weapons?",
        "Best COD scorestreak?",
        "Which COD had the best multiplayer progression system?",
        "Favorite COD multiplayer perk?",
        "Which COD had the best Zombies maps overall?",
        "Best COD melee weapon?"
    ],
    "general": [
        "If you could have dinner with any fictional character, who?",
        "What's the weirdest food combination you enjoy?",
        "If you woke up with a superpower tomorrow, what would it be?",
        "What’s your guilty pleasure TV show?",
        "If you won the lottery, what’s the first thing you’d buy?",
        "What’s the most underrated hobby?",
        "What’s your favorite childhood memory?",
        "If you could instantly learn any skill, what would it be?",
        "What’s the funniest meme you’ve seen recently?",
        "If you could live anywhere in the world, where?",
        "What’s your go-to comfort food?",
        "If you could time travel, past or future?",
        "What’s your favorite holiday tradition?",
        "If you could swap lives with someone for a day, who?",
        "What’s the best advice you’ve ever received?",
        "If you could own any animal as a pet, what would it be?",
        "What’s your favorite movie quote?",
        "If you could only eat one cuisine forever, which?",
        "What’s your dream job?",
        "If you could meet any historical figure, who?",
        "What’s your favorite season?",
        "If you could master one instrument, which?",
        "What’s your go-to karaoke song?",
        "If you could change one thing about the world, what?",
        "What’s your favorite board game?",
        "If you could live in any fictional universe, which?",
        "What’s your favorite ice cream flavor?",
        "If you could instantly speak any language, which?",
        "What’s your favorite childhood cartoon?",
        "If you could redo one day in your life, which?",
        "What’s your favorite snack?",
        "If you could be famous for anything, what?",
        "What’s your favorite book?",
        "If you could teleport anywhere right now, where?",
        "What’s your favorite outdoor activity?",
        "If you could design your dream house, what’s in it?",
        "What’s your favorite video game?",
        "If you could relive one year, which?",
        "What’s your favorite dessert?",
        "If you could be invisible for a day, what would you do?",
        "What’s your favorite childhood toy?"
    ]
}

# ==================== DATABASE SCHEMA ====================
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

# ==================== DB HELPERS ====================
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(_SCHEMA_SQL)
        await db.commit()

async def seed_default_questions(guild_id: int):
    """Insert default categories/questions only if the category doesn't already exist for the guild."""
    async with aiosqlite.connect(DB_PATH) as db:
        for category, questions in DEFAULT_QUESTIONS.items():
            cur = await db.execute("SELECT 1 FROM categories WHERE guild_id = ? AND name = ? LIMIT 1", (guild_id, category))
            exists = await cur.fetchone()
            if exists:
                continue
            await db.execute("INSERT INTO categories (guild_id, name) VALUES (?, ?)", (guild_id, category))
            ts = int(time.time())
            for q in questions:
                await db.execute(
                    "INSERT INTO questions (guild_id, category, author_id, content, created_at) VALUES (?, ?, ?, ?, ?)",
                    (guild_id, category, 0, q, ts)
                )
        await db.commit()

async def add_category(guild_id: int, name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO categories (guild_id, name) VALUES (?, ?)", (guild_id, name))
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

async def get_categories(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT name FROM categories WHERE guild_id = ?", (guild_id,))
        rows = await cur.fetchall()
        return [r["name"] for r in rows]

async def add_revive_channel(guild_id: int, channel_id: int, category: str, threshold: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO revive_channels (guild_id, channel_id, category, inactivity_threshold, last_message_ts) VALUES (?, ?, ?, ?, ?)",
            (guild_id, channel_id, category, threshold, int(time.time())),
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

# ==================== AUTOCOMPLETE ====================
async def category_autocomplete(interaction: discord.Interaction, current: str):
    names = await get_categories(interaction.guild_id)
    return [
        app_commands.Choice(name=name, value=name)
        for name in names if current.lower() in name.lower()
    ]

# ==================== CHANNEL RESOLUTION ====================
CHANNEL_MENTION_RE = re.compile(r"<#(\d+)>")

async def resolve_text_channel(guild: Optional[discord.Guild], raw: str) -> Optional[discord.TextChannel]:
    if not guild or not raw:
        return None
    raw = raw.strip()
    # mention like <#123>
    m = CHANNEL_MENTION_RE.match(raw)
    if m:
        try:
            cid = int(m.group(1))
            ch = guild.get_channel(cid)
            return ch if isinstance(ch, discord.TextChannel) else None
        except Exception:
            return None
    # numeric id
    if raw.isdigit():
        try:
            ch = guild.get_channel(int(raw))
            return ch if isinstance(ch, discord.TextChannel) else None
        except Exception:
            return None
    # exact name match
    for ch in guild.text_channels:
        if ch.name.lower() == raw.lower():
            return ch
    # partial match fallback
    raw_l = raw.lower()
    for ch in guild.text_channels:
        if raw_l in ch.name.lower():
            return ch
    return None

# ==================== BACKGROUND LOOP ====================
async def check_inactivity_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                db.row_factory = aiosqlite.Row
                cur = await db.execute("SELECT * FROM revive_channels")
                rows = await cur.fetchall()
            now_ts = int(time.time())
            for row in rows:
                try:
                    if now_ts - row["last_message_ts"] >= row["inactivity_threshold"]:
                        channel = bot.get_channel(row["channel_id"])
                        if channel and isinstance(channel, discord.TextChannel):
                            questions = await get_questions(row["guild_id"], row["category"])
                            if questions:
                                q = random.choice(questions)
                                await channel.send(f"💡 {q}")
                                async with aiosqlite.connect(DB_PATH) as db:
                                    await db.execute(
                                        "UPDATE revive_channels SET last_message_ts = ? WHERE id = ?",
                                        (now_ts, row["id"]),
                                    )
                                    await db.commit()
                except Exception:
                    logger.exception("Failed to process revive row id=%s", row.get("id"))
        except Exception:
            logger.exception("Error in inactivity loop")
        await asyncio.sleep(60)

# ==================== SLASH COMMANDS ====================
@tree.command(name="help", description="Show all available commands and what they do")
async def help_cmd(interaction: discord.Interaction):
    help_text = (
        "📖 **ChatPulse Bot Commands**\n\n"
        "🔹 `/ping` — Test if the bot responds.\n"
        "🔹 `/add_category <name>` — Add a new question category. (Admins only)\n"
        "🔹 `/add_question <category> <content>` — Add a question to a category. (Admins only)\n"
        "🔹 `/delete_question <category> <content>` — Delete a question from a category. (Admins only)\n"
        "🔹 `/list_questions <category>` — List questions in a category.\n"
        "🔹 `/setup_revive` — Configure revive logic for a channel (picker or typed input). (Admins only)\n"
        "🔹 `/remove_revive` — Remove revive logic from a channel. (Admins only)\n"
        "🔹 `/revive_now` — Trigger a manual revive message. (Admins only)\n"
        "🔹 `/status` — Show revive channel status and thresholds.\n"
        "🔹 `/reset_categories` — Re-add default categories/questions for this server. (Admins only)\n"
        "🔹 `/debug_categories` — Show categories currently in the DB for this server. (Admins only)\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@tree.command(name="ping", description="Test if bot responds")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="add_category", description="Add a new question category")
@app_commands.default_permissions(manage_guild=True)
async def add_category_cmd(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True)
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

@tree.command(name="delete_question", description="Delete a question from a category")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def delete_question_cmd(interaction: discord.Interaction, category: str, content: str):
    await interaction.response.defer(ephemeral=True)
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute(
                "SELECT id FROM questions WHERE guild_id = ? AND category = ? AND content = ? LIMIT 1",
                (interaction.guild_id, category, content)
            )
            row = await cur.fetchone()
            if not row:
                await interaction.followup.send(f"⚠️ No matching question found in '{category}'.", ephemeral=True)
                return
            await db.execute("DELETE FROM questions WHERE id = ?", (row[0],))
            await db.commit()
        await interaction.followup.send(f"❌ Question '{content}' deleted from '{category}'.", ephemeral=True)
    except Exception:
        logger.exception("delete_question failed")
        await interaction.followup.send("❌ Failed to delete question.", ephemeral=True)

@tree.command(name="list_questions", description="List questions in a category")
@app_commands.autocomplete(category=category_autocomplete)
async def list_questions_cmd(interaction: discord.Interaction, category: str):
    await interaction.response.defer(ephemeral=True)
    try:
        qs = await get_questions(interaction.guild_id, category)
        if not qs:
            await interaction.followup.send("No questions found.", ephemeral=True)
            return
        await interaction.followup.send("\n".join([f"- {q}" for q in qs[:50]]), ephemeral=True)
    except Exception:
        logger.exception("list_questions failed")
        await interaction.followup.send("❌ Failed to list questions.", ephemeral=True)

@tree.command(name="reset_categories", description="Reseed default categories/questions for this server")
@app_commands.default_permissions(manage_guild=True)
async def reset_categories(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        await seed_default_questions(interaction.guild_id)
        await interaction.followup.send("✅ Default categories and questions re-added (if missing).", ephemeral=True)
    except Exception:
        logger.exception("reset_categories failed")
        await interaction.followup.send("❌ Failed to reset categories.", ephemeral=True)

@tree.command(name="debug_categories", description="List categories currently in the DB for this server")
@app_commands.default_permissions(manage_guild=True)
async def debug_categories(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        cats = await get_categories(interaction.guild_id)
        await interaction.followup.send(f"Categories: {', '.join(cats) if cats else 'None'}", ephemeral=True)
    except Exception:
        logger.exception("debug_categories failed")
        await interaction.followup.send("❌ Failed to fetch categories.", ephemeral=True)

# ----------------- setup_revive (picker + typed input) -----------------
@tree.command(name="setup_revive", description="Set up revive for a channel (picker or typed input)")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def setup_revive(
    interaction: discord.Interaction,
    channel: Optional[discord.abc.GuildChannel] = None,   # channel picker
    channel_str: Optional[str] = None,                   # typed input
    category: str = "general",
    hours: int = 1
):
    await interaction.response.defer(ephemeral=True)
    try:
        ch = None
        # Prefer the picker
        if channel is not None:
            if isinstance(channel, discord.TextChannel):
                ch = channel
            else:
                await interaction.followup.send("⚠️ Please pick a normal text channel (not a forum, category, or voice channel).", ephemeral=True)
                return
        elif channel_str:
            ch = await resolve_text_channel(interaction.guild, channel_str)
            if not ch:
                await interaction.followup.send(
                    "⚠️ Could not resolve that channel. Use the channel picker, mention the channel like <#ID>, or provide exact name/ID.",
                    ephemeral=True
                )
                return
        else:
            await interaction.followup.send("⚠️ You must provide a channel (use the picker or type a channel name/ID).", ephemeral=True)
            return

        cats = await get_categories(interaction.guild_id)
        if category not in cats:
            await interaction.followup.send(f"⚠️ Category '{category}' not found. Add it with /add_category or run /reset_categories.", ephemeral=True)
            return

        threshold = max(60, hours * 3600)
        await add_revive_channel(interaction.guild_id, ch.id, category, threshold)
        await interaction.followup.send(f"✅ Revive set for {ch.mention} with category '{category}' after {hours} hour(s).", ephemeral=True)
    except Exception:
        logger.exception("setup_revive failed")
        await interaction.followup.send("❌ Failed to set revive — check the bot logs.", ephemeral=True)

# ----------------- remove_revive (picker + typed input) -----------------
@tree.command(name="remove_revive", description="Remove revive from a channel (picker or typed input)")
@app_commands.default_permissions(manage_guild=True)
async def remove_revive_cmd(
    interaction: discord.Interaction,
    channel: Optional[discord.abc.GuildChannel] = None,
    channel_str: Optional[str] = None
):
    await interaction.response.defer(ephemeral=True)
    try:
        ch = None
        if channel is not None:
            if isinstance(channel, discord.TextChannel):
                ch = channel
            else:
                await interaction.followup.send("⚠️ Please pick a normal text channel.", ephemeral=True)
                return
        elif channel_str:
            ch = await resolve_text_channel(interaction.guild, channel_str)
            if not ch:
                await interaction.followup.send("⚠️ Could not resolve that channel. Use the channel picker or mention the channel.", ephemeral=True)
                return
        else:
            await interaction.followup.send("⚠️ You must provide a channel (use the picker or type a channel name/ID).", ephemeral=True)
            return

        await remove_revive_channel(interaction.guild_id, ch.id)
        await interaction.followup.send(f"❌ Revive removed from {ch.mention}.", ephemeral=True)
    except Exception:
        logger.exception("remove_revive failed")
        await interaction.followup.send("❌ Failed to remove revive — check the bot logs.", ephemeral=True)

# ----------------- revive_now (picker + typed input) -----------------
@tree.command(name="revive_now", description="Trigger a manual revive (picker or typed input)")
@app_commands.default_permissions(manage_guild=True)
@app_commands.autocomplete(category=category_autocomplete)
async def revive_now(
    interaction: discord.Interaction,
    channel: Optional[discord.abc.GuildChannel] = None,
    channel_str: Optional[str] = None,
    category: str = "general"
):
    await interaction.response.defer(ephemeral=True)
    try:
        ch = None
        if channel is not None:
            if isinstance(channel, discord.TextChannel):
                ch = channel
            else:
                await interaction.followup.send("⚠️ Please pick a normal text channel.", ephemeral=True)
                return
        elif channel_str:
            ch = await resolve_text_channel(interaction.guild, channel_str)
            if not ch:
                await interaction.followup.send("⚠️ Could not resolve that channel. Use the channel picker or mention the channel.", ephemeral=True)
                return
        else:
            await interaction.followup.send("⚠️ You must provide a channel (use the picker or type a channel name/ID).", ephemeral=True)
            return

        qs = await get_questions(interaction.guild_id, category)
        if not qs:
            await interaction.followup.send(f"No questions available in '{category}'.", ephemeral=True)
            return
        q = random.choice(qs)
        await ch.send(f"💡 {q}")
        await interaction.followup.send("✅ Revive message sent.", ephemeral=True)
    except Exception:
        logger.exception("revive_now failed")
        await interaction.followup.send("❌ Failed to send revive — check the bot logs.", ephemeral=True)

@tree.command(name="status", description="Show bot status")
async def status(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        channels = await get_revive_channels(interaction.guild_id)
        if not channels:
            await interaction.followup.send("No revive channels configured.", ephemeral=True)
            return
        lines = []
        for ch in channels:
            channel_obj = interaction.guild.get_channel(ch["channel_id"])
            mention = channel_obj.mention if channel_obj else f"<#{ch['channel_id']}>"
            # show threshold in hours if divisible, else in minutes
            th = ch["inactivity_threshold"]
            if th % 3600 == 0:
                th_display = f"{th // 3600}h"
            else:
                th_display = f"{th // 60}m"
            lines.append(f"{mention} → Category: {ch['category']}, Threshold: {th_display}")
        await interaction.followup.send("\n".join(lines), ephemeral=True)
    except Exception:
        logger.exception("status failed")
        await interaction.followup.send("❌ Failed to fetch status.", ephemeral=True)

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    logger.info("Bot ready: %s", bot.user)
    try:
        await init_db()
    except Exception:
        logger.exception("Failed to initialize DB")
    # seed defaults for all guilds (only inserts if missing)
    for guild in bot.guilds:
        try:
            await seed_default_questions(guild.id)
        except Exception:
            logger.exception("Failed to seed defaults for guild %s", guild.id)
    # start background loop
    bot.loop.create_task(check_inactivity_loop())
    # global sync
    try:
        await tree.sync()
        logger.info("Commands synced globally.")
    except Exception:
        logger.exception("Failed to sync commands globally.")

# ==================== RUN ====================
if __name__ == "__main__":
    if TOKEN == "YOUR_TOKEN":
        logger.warning("No token provided. Set DISCORD_BOT_TOKEN or TOKEN environment variable.")
    bot.run(TOKEN)
