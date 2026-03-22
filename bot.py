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
"Do you prefer hardcore or peaceful?",
        "What's your go-to biome to build in?",
        "Creeper or skeleton - which is more annoying?",
    ],
    "cod": [
        "Favorite COD game of all time?",
        
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
"Best COD melee weapon?",
"Which COD had the best multiplayer customization?",
"Favorite COD multiplayer operator?",
"Which COD had the best Zombies Easter egg quests?",
"Best COD battle royale mode?",
"Which COD had the best multiplayer gun variety?",
"Favorite COD multiplayer tactical equipment?",
"Which COD had the best Zombies bosses?",
"Best COD multiplayer lethal equipment?",
"Which COD had the best multiplayer maps overall?",
"Favorite COD multiplayer scorestreak?",
"Which COD had the best Zombies progression?",
"Best COD multiplayer melee weapon?",
"Which COD had the best multiplayer gun balance?",
"Favorite COD multiplayer class?",
"Which COD had the best Zombies mechanics?",
"Best COD multiplayer operator?",
"Which COD had the best multiplayer perks?",
"Favorite COD multiplayer progression system?",
"Which COD had the best Zombies maps pack?",
"Best COD multiplayer customization option?",
"Which COD had the best multiplayer scorestreaks?",
"Favorite COD multiplayer gun?",
"Which COD had the best Zombies Easter egg rewards?",
"Best COD multiplayer tactical option?",
"Which COD had the best multiplayer lethal options?",
"Favorite COD multiplayer melee weapon?",
"Which COD had the best Zombies maps design?",
"Best COD multiplayer progression option?",
"Which COD had the best multiplayer customization system?",
"Favorite COD multiplayer perk setup?",
"Which COD had the best Zombies maps pack overall?",
"Best COD multiplayer scorestreak option?",
"Which COD had the best multiplayer gun mechanics?",
"Favorite COD multiplayer operator skin?",
"Which COD had the best Zombies maps Easter eggs?",
"Best COD multiplayer lethal option?",
"Which COD had the best multiplayer tactical mechanics?",
"Favorite COD multiplayer melee option?",
"Which COD had the best Zombies maps bosses?",
"Best COD multiplayer customization skin?",
"Which COD had the best multiplayer progression mechanics?",
"Favorite COD multiplayer scorestreak setup?",
"Which COD had the best Zombies maps weapons?",
        "SMG or Assault Rifle?",
        "Hardpoint or Search & Destroy?",
    ],
    "general": [
        "If you could have dinner with any fictional character, who?",
        
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
"What’s your favorite childhood toy?",
"If you could swap jobs with anyone, who?",
"What’s your favorite sport to watch?",
"If you could change your name, what would it be?",
"What’s your favorite pizza topping?",
"If you could be any age forever, which?",
"What’s your favorite hobby?",
"If you could have any car, which?",
"What’s your favorite song?",
"If you could erase one fear, which?",
"What’s your favorite drink?",
"If you could be in any movie, which?",
"What’s your favorite holiday?",
"If you could be any animal, which?",
"What’s your favorite childhood game?",
"If you could live in any era, which?",
"What’s your favorite TV series?",
"If you could invent something, what?",
"What’s your favorite fruit?",
"If you could be a superhero, what’s your power?",
"What’s your favorite place to relax?",
"If you could be on any reality show, which?",
"What’s your favorite fast food?",
"If you could change one law, which?",
"What’s your favorite childhood book?",
"If you could be any profession for a week, which?",
"What’s your favorite candy?",
"If you could swap talents with someone, who?",
"What’s your favorite childhood song?",
"If you could live without one modern invention, which?",
"What’s your favorite breakfast?",
"If you could be any character in a book, who?",
"What’s your favorite childhood movie?",
"If you could have any job perk, what?",
"What’s your favorite childhood snack?",
"If you could be any celebrity’s friend, who?",
"What’s your favorite childhood TV show?",
"If you could change one thing about yourself, what?",
"What’s your favorite childhood place?",
"If you could be any mythical creature, which?",
"What’s your favorite childhood holiday?",
"If you could relive one childhood day, which?",
"What’s your favorite childhood sport?",
"If you could be any cartoon character, who?",
"What’s your favorite childhood memory with friends?",
"If you could have any childhood toy back, which?",
"What’s your favorite childhood family tradition?",
"If you could relive one childhood trip, which?",
"What’s your favorite childhood school subject?",
"If you could be any childhood hero, who?",
"What’s your favorite childhood birthday gift?",
"If you could relive one childhood summer, which?",
"What’s your favorite childhood teacher?",
"If you could be any childhood fictional character, who?",
"What’s your favorite childhood dream?",
"If you could relive one childhood game, which?",
"What’s your favorite childhood laugh?",
"If you could relive one childhood adventure, which?",
"What’s your favorite childhood secret?",
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
        await interaction.response.send_message("\n".join([f"- {q}" for q in qs[:50]]), ephemeral=True)

@tree.command(name="reset_categories", description="Reseed default categories/questions for this server")
@app_commands.default_permissions(manage_guild=True)
async def reset_categories(interaction: discord.Interaction):
    await seed_default_questions(interaction.guild_id)
    await interaction.response.send_message("✅ Categories have been reset and default questions re-added.", ephemeral=True)


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
    # 👇 sync globally instead of per guild
    await tree.sync()
    print(f"Bot ready: {bot.user}")


# ==================== RUN ====================
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ No bot token found in environment variables.")

