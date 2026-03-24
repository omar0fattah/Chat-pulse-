from discord.ui import View, button
import os
import random
import aiosqlite
import json
import discord
from discord import app_commands, Embed
from discord.ext import tasks, commands
import time
revive_cooldowns = {}
metrics_data = {}  # {guild_id: count of revives fired}

SETTINGS_FILE = "revive_settings.json"

# Built-in question pools (locked, cannot be deleted)
BUILTIN_POOLS = {
    "general": [
        "👀 What’s everyone up to today?",
                "🌍 If you could live anywhere, where would it be?",
        "🎶 What’s your favorite song right now?",
        "📚 What book are you currently reading?",
        "🎬 Favorite movie of all time?",
        "🎮 What game do you never get tired of?",
        "📱 Which app do you use the most?",
        "🏖️ Dream vacation spot?",
        "🐶 Do you prefer cats or dogs?",
        "☕ Coffee or tea?",
        "📺 What show are you binge-watching?",
        "🎤 Who’s your favorite musician?",
        "🚗 What’s your dream car?",
        "💻 PC or console gaming?",
        "📸 Do you like taking photos?",
        "🎨 Do you enjoy drawing or painting?",
        "🛒 Online shopping or in-store?",
        "🏀 Favorite sport to watch?",
        "⚽ Favorite sport to play?",
        "🎯 What’s a skill you want to learn?",
        "📖 Do you prefer fiction or non-fiction?",
        "🎧 Do you listen to podcasts?",
        "🕹️ Retro games or modern games?",
        "🍕 Pineapple on pizza: yes or no?",
        "💡 What’s a random fun fact you know?",
        "🌌 Do you believe in aliens?",
        "🎉 Favorite holiday?",
        "🎂 How do you celebrate birthdays?",
        "🛏️ Do you nap during the day?",
        "🎁 Best gift you’ve ever received?",
        "🎁 Best gift you’ve ever given?",
        "🏡 Do you prefer city or countryside?",
        "🌳 Do you like camping?",
        "🏖️ Beach or mountains?",
        "💡 Morning person or night owl?",
        "📷 Do you prefer selfies or group photos?",
        "🛠️ What’s a DIY project you’ve done?",
        "🎓 What subject did you love in school?",
        "🎓 What subject did you hate in school?",
        "💼 What’s your dream job?",
        "💼 What’s your current job?",
        "💼 Do you enjoy your work?",
        "🧑‍🏫 Who was your favorite teacher?",
        "🧑‍🏫 Who was your least favorite teacher?",
        "📈 Do you follow the stock market?",
        "💸 Do you prefer saving or spending?",
        "💳 Do you use cash or card?",
        "🏦 Do you trust banks?",
        "🏦 Do you invest in crypto?",
        "📊 Do you budget monthly?",
        "📊 Do you track expenses?",
        "🧘 Do you meditate?",
        "🏋️ Do you exercise regularly?",
        "🚴 Do you cycle?",
        "🏊 Do you swim?",
        "🏃 Do you run?",
        "🧗 Do you hike?",
        "🛹 Do you skateboard?",
        "🎲 Do you play board games?",
        "♟️ Do you play chess?",
        "🃏 Do you play card games?",
        "🎯 Do you play darts?",
        "🎳 Do you bowl?",
        "🎱 Do you play pool?",
        "🎮 Do you play mobile games?",
        "🎮 Do you play PC games?",
        "🎮 Do you play console games?",
        "🎮 Do you play VR games?",
        "📱 Do you use social media?",
        "📱 Which social media do you use most?",
        "📱 Do you prefer Instagram or TikTok?",
        "📱 Do you prefer Twitter or Facebook?",
        "📱 Do you prefer Snapchat or WhatsApp?",
        "📱 Do you prefer Discord or Reddit?",
        "📱 Do you prefer YouTube or Twitch?",
        "📱 Do you prefer Netflix or Disney+?",
        "📱 Do you prefer Spotify or Apple Music?",
        "📱 Do you prefer Kindle or physical books?",
        "📱 Do you prefer podcasts or audiobooks?",
        "📱 Do you prefer texting or calling?",
        "📱 Do you prefer email or chat?",
        "📱 Do you prefer video calls or voice calls?",
        "📱 Do you prefer group chats or DMs?",
        "📱 Do you prefer memes or reels?",
        "📱 Do you prefer stories or posts?",
        "📱 Do you prefer Linux or Windows?",
        "📱 Do you prefer Chrome or Firefox?",
        "📱 Do you prefer Edge or Safari?",
        "📱 Do you prefer Google or Bing?",
        "📱 Do you prefer AI tools or manual work?",
        "📱 Do you prefer smart homes or traditional homes?",
        "📱 Do you prefer electric cars or gas cars?",
        "📱 Do you prefer trains or planes?",
        "📱 Do you prefer buses or taxis?",
        "📱 Do you prefer walking or cycling?",
        "📱 Do you prefer city life or rural life?",
        "📱 Do you prefer hot weather or cold weather?",
        "📱 Do you prefer rain or snow?",
        "🔥 Share the last song you listened to!",
        "💡 What’s a random fun fact you know?"
    ],
    "apex": [
              # Beginner (33)
        "🎯 Who was the first legend you tried?",
        "🔫 What’s your favorite starter weapon?",
        "🛡️ Do you prefer shields or health items first?",
        "🏃 Do you like aggressive or passive playstyles?",
        "📍 What’s your favorite landing spot?",
        "🎮 Do you play solo or with friends?",
        "🗺️ Which map do you find easiest?",
        "💡 Which legend ability do you use most?",
        "🎯 Do you prefer close‑range or long‑range fights?",
        "🛠️ Do you customize your controls or keep default?",
        "🔊 Do you use voice chat often?",
        "📦 Do you loot fast or carefully?",
        "🪂 Do you hot‑drop or land safe?",
        "🎯 Do you practice aim in the Firing Range?",
        "🛡️ Do you carry more batteries or cells?",
        "🔫 Do you prefer SMGs or ARs?",
        "🎯 Do you like shotguns or snipers?",
        "🛡️ Do you upgrade armor or weapons first?",
        "🎮 Do you play ranked or pubs more?",
        "🗺️ Which season was your favorite so far?",
        "🎯 Which legend do you find easiest to learn?",
        "🛡️ Do you prefer healing items or grenades?",
        "🎯 Do you like playing support or damage?",
        "🗺️ Which map do you struggle with most?",
        "🎯 Do you prefer crafting or looting?",
        "🛡️ Do you like gold loot items?",
        "🎯 Do you prefer fast or slow rotations?",
        "🛡️ Do you revive teammates quickly or wait?",
        "🎯 Do you prefer playing with randoms or friends?",
        "🛡️ Do you like experimenting with new legends?",
        "🎯 Do you prefer training mode or live matches?",
        "🛡️ Do you prefer skins or badges?",
        "🎯 Do you prefer casual or competitive play?",

        # Intermediate (33)
        "🛡️ How do you manage shield swaps in fights?",
        "🎯 What’s your go‑to weapon combo?",
        "🗺️ Which rotations do you prefer mid‑game?",
        "📦 Do you prioritize loot or positioning?",
        "🎯 How do you counter third parties?",
        "🛡️ Which legend do you think is underrated?",
        "🎯 Do you use grenades often?",
        "🛡️ How do you balance healing vs fighting?",
        "🎯 Do you prefer crafting or looting?",
        "🗺️ Which map rotation do you struggle with?",
        "🎯 How do you decide when to push?",
        "🛡️ Do you prefer defensive or offensive legends?",
        "🎯 Which legend ult do you find most impactful?",
        "🗺️ Do you rotate early or late?",
        "🎯 How do you handle being the last alive?",
        "🛡️ Do you prefer gold armor or red armor?",
        "🎯 Which weapon do you think is overrated?",
        "🗺️ Do you memorize loot spawns?",
        "🎯 How do you manage ammo types?",
        "🛡️ Do you prefer mobile respawn beacons or banners?",
        "🎯 How do you counter scan legends?",
        "🛡️ Do you prefer zone or edge play?",
        "🎯 How do you manage comms in mid‑game?",
        "🛡️ Which legend ult do you save for end‑game?",
        "🎯 How do you balance KP vs placement?",
        "🗺️ Which map POIs are strongest for ranked?",
        "🎯 How do you counter rat squads?",
        "🛡️ Do you prefer controller or M&K?",
        "🎯 How do you train recoil control?",
        "🛡️ Which legend do you flex into ranked?",
        "🎯 How do you adapt to patch changes?",
        "🛡️ Do you prefer LAN or online tournaments?",
        "🎯 How do you manage squad roles?",

        # Pro (34)
        "🎯 How do you coordinate pushes with your squad?",
        "🛡️ Which legend combos do you run in ranked?",
        "🎯 How do you counter meta team comps?",
        "🗺️ Which rotations give you the best win rate?",
        "🎯 How do you manage end‑game positioning?",
        "🛡️ Do you prefer anchoring or entry fragging?",
        "🎯 How do you track enemy cooldowns?",
        "🛡️ Which legend ult do you save for end‑game?",
        "🎯 How do you balance KP vs placement?",
        "🗺️ Which map POIs are strongest for tournaments?",
        "🎯 How do you counter scan legends?",
        "🛡️ Do you prefer controller or M&K at high level?",
        "🎯 How do you train recoil control?",
        "🛡️ Which legend do you flex into scrims?",
        "🎯 How do you manage comms under pressure?",
        "🛡️ Do you prefer zone or edge play?",
        "🎯 How do you counter rat squads?",
        "🛡️ Which weapon do you rely on in finals?",
        "🎯 How do you adapt to patch changes?",
        "🛡️ Do you prefer LAN or online tournaments?",
        "🎯 How do you coordinate with pro teammates?",
        "🛡️ Which legend do you ban in scrims?",
        "🎯 How do you counter controller aim assist?",
        "🛡️ Which weapon do you think defines the meta?",
        "🎯 How do you manage rotations in ALGS?",
        "🛡️ Do you prefer edge fights or zone holds?",
        "🎯 How do you counter Valk ult rotations?",
        "🛡️ Which legend ult wins most end‑games?",
        "🎯 How do you manage comms in finals?",
        "🛡️ Which weapon combo is best for pro play?",
        "🎯 How do you counter Seer scans?",
        "🛡️ Which legend do you main in tournaments?",
        "🎯 How do you adapt to new maps?",
        "🛡️ Which legend ult is most clutch?"

    ],
    "cod": [
               # Beginner (33)
        "🔫 What’s your favorite starting weapon?",
        "🎯 Do you prefer assault rifles or SMGs?",
        "💣 What’s your favorite map to learn on?",
        "🛡️ Do you use perks often?",
        "🎮 Do you play campaign or multiplayer more?",
        "🎯 Do you prefer Team Deathmatch or Domination?",
        "🔫 Do you customize your loadouts?",
        "🎯 Do you prefer close‑range or long‑range fights?",
        "💣 Do you use grenades or flashbangs more?",
        "🎯 Do you play hardcore or core modes?",
        "🎮 Do you play solo or with friends?",
        "🗺️ Which map do you find easiest?",
        "🎯 Do you prefer killstreaks or scorestreaks?",
        "🔫 Do you use shotguns often?",
        "🎯 Do you prefer sniping or rushing?",
        "💣 Do you like explosives?",
        "🎯 Do you prefer tactical or lethal equipment?",
        "🛡️ Do you use armor plates often?",
        "🎯 Do you prefer quickscoping or hardscoping?",
        "🔫 Do you use pistols or melee?",
        "🎯 Do you prefer UAV or Counter‑UAV?",
        "💣 Do you prefer frag grenades or semtex?",
        "🎯 Do you prefer stun grenades or flashbangs?",
        "🛡️ Do you prefer lightweight or heavy perks?",
        "🎯 Do you prefer sprinting or crouching?",
        "🗺️ Do you prefer small maps or large maps?",
        "🎯 Do you prefer free‑for‑all or team modes?",
        "🔫 Do you prefer burst or auto weapons?",
        "🎯 Do you prefer iron sights or optics?",
        "💣 Do you prefer claymores or mines?",
        "🎯 Do you prefer silencers or extended mags?",
        "🛡️ Do you prefer fast reload or extra ammo?",
        "🎯 Do you prefer campaign or zombies?",

        # Intermediate (33)
        "🎯 What’s your go‑to weapon combo?",
        "🛡️ How do you manage perks in matches?",
        "🎯 Do you prefer balanced or specialized loadouts?",
        "🗺️ Which rotations do you prefer mid‑game?",
        "🎯 How do you counter campers?",
        "🛡️ Which perk do you think is underrated?",
        "🎯 Do you use killstreaks strategically?",
        "🛡️ How do you balance healing vs fighting?",
        "🎯 Do you prefer rushing or holding angles?",
        "🗺️ Which map rotation do you struggle with?",
        "🎯 How do you decide when to push?",
        "🛡️ Do you prefer defensive or offensive perks?",
        "🎯 Which killstreak do you find most impactful?",
        "🗺️ Do you rotate early or late?",
        "🎯 How do you handle being the last alive?",
        "🛡️ Do you prefer armor plates or extra ammo?",
        "🎯 Which weapon do you think is overrated?",
        "🗺️ Do you memorize spawn points?",
        "🎯 How do you manage ammo types?",
        "🛡️ Do you prefer tactical insertion or respawn?",
        "🎯 How do you counter snipers?",
        "🛡️ Do you prefer zone control or roaming?",
        "🎯 How do you manage comms in mid‑game?",
        "🛡️ Which killstreak do you save for end‑game?",
        "🎯 How do you balance kills vs objectives?",
        "🗺️ Which map POIs are strongest for Domination?",
        "🎯 How do you counter riot shields?",
        "🛡️ Do you prefer controller or M&K?",
        "🎯 How do you train recoil control?",
        "🛡️ Which perk do you flex into ranked?",
        "🎯 How do you adapt to patch changes?",
        "🛡️ Do you prefer LAN or online tournaments?",
        "🎯 How do you manage squad roles?",

        # Pro (34)
        "🎯 How do you coordinate pushes with your squad?",
        "🛡️ Which perk combos do you run in ranked?",
        "🎯 How do you counter meta loadouts?",
        "🗺️ Which rotations give you the best win rate?",
        "🎯 How do you manage end‑game positioning?",
        "🛡️ Do you prefer anchoring or entry fragging?",
        "🎯 How do you track enemy cooldowns?",
        "🛡️ Which killstreak do you save for end‑game?",
        "🎯 How do you balance kills vs placement?",
        "🗺️ Which map POIs are strongest for tournaments?",
        "🎯 How do you counter pro snipers?",
        "🛡️ Do you prefer controller or M&K at high level?",
        "🎯 How do you train recoil control?",
        "🛡️ Which perk do you flex into scrims?",
        "🎯 How do you manage comms under pressure?",
        "🛡️ Do you prefer zone or edge play?",
        "🎯 How do you counter rat squads?",
        "🛡️ Which weapon do you rely on in finals?",
        "🎯 How do you adapt to patch changes?",
        "🛡️ Do you prefer LAN or online tournaments?",
        "🎯 How do you coordinate with pro teammates?",
        "🛡️ Which perk do you ban in scrims?",
        "🎯 How do you counter controller aim assist?",
        "🛡️ Which weapon do you think defines the meta?",
        "🎯 How do you manage rotations in CDL?",
        "🛡️ Do you prefer edge fights or zone holds?",
        "🎯 How do you counter spawn traps?",
        "🛡️ Which killstreak wins most end‑games?",
        "🎯 How do you manage comms in finals?",
        "🛡️ Which weapon combo is best for pro play?",
        "🎯 How do you counter meta perks?",
        "🛡️ Which perk do you main in tournaments?",
        "🎯 How do you adapt to new maps?",
        "🛡️ Which killstreak is most clutch?"

    ],
    "minecraft": [
                # Beginner (33)
        "⛏️ Do you prefer Survival or Creative mode?",
        "🏠 What was your first Minecraft build?",
        "🐄 Do you farm animals or just explore?",
        "🌍 Do you prefer plains or forests?",
        "🪵 Do you build with wood or stone first?",
        "🔥 Have you ever died in lava?",
        "💎 What’s the first ore you mine?",
        "🐉 Have you ever fought the Ender Dragon?",
        "🛏️ Do you always carry a bed?",
        "🌌 Do you explore caves or stay above ground?",
        "🪓 Do you prefer axes or swords?",
        "🛡️ Do you craft shields early?",
        "🪨 Do you prefer cobblestone or smooth stone?",
        "🌳 Do you plant trees near your base?",
        "🐟 Do you fish for food?",
        "🍞 Do you farm wheat or potatoes?",
        "🐷 Do you keep pigs or cows?",
        "🐔 Do you farm chickens?",
        "🐑 Do you dye sheep wool?",
        "🛠️ Do you craft tools or armor first?",
        "🪙 Do you trade with villagers?",
        "🏠 Do you build underground or above ground?",
        "🛤️ Do you use minecarts?",
        "🌊 Do you build near water?",
        "🪨 Do you prefer caves or cliffs?",
        "🛏️ Do you sleep every night?",
        "🌌 Do you explore the Nether early?",
        "🐺 Do you tame wolves?",
        "🐴 Do you ride horses?",
        "🐱 Do you tame cats?",
        "🛠️ Do you craft enchantment tables early?",
        "🪨 Do you prefer stone tools or iron tools?",
        "🛡️ Do you fight mobs at night?",

        # Intermediate (33)
        "🛠️ What’s your go‑to enchantment setup?",
        "🛡️ Do you prefer diamond or netherite armor?",
        "🗺️ Do you explore strongholds often?",
        "🐉 How do you prepare for the Ender Dragon?",
        "🔥 Do you build Nether bases?",
        "🛤️ Do you use redstone for automation?",
        "🪙 Do you farm villagers for trades?",
        "🛠️ Do you prefer brewing potions or enchanting?",
        "🛡️ Do you fight the Wither?",
        "🗺️ Do you explore ocean monuments?",
        "🐠 Do you farm fish or coral?",
        "🛠️ Do you craft beacons?",
        "🛡️ Do you use Elytra often?",
        "🗺️ Do you raid bastions?",
        "🔥 Do you use fire resistance potions?",
        "🛠️ Do you build XP farms?",
        "🛡️ Do you prefer ranged or melee combat?",
        "🗺️ Do you explore woodland mansions?",
        "🐝 Do you farm bees?",
        "🛠️ Do you build automatic crop farms?",
        "🛡️ Do you use tridents?",
        "🗺️ Do you explore desert temples?",
        "🐢 Do you farm turtles?",
        "🛠️ Do you craft conduits?",
        "🛡️ Do you use crossbows?",
        "🗺️ Do you explore igloos?",
        "🐇 Do you farm rabbits?",
        "🛠️ Do you build mob grinders?",
        "🛡️ Do you use shields in PvP?",
        "🗺️ Do you explore pillager outposts?",
        "🐎 Do you breed horses?",
        "🛠️ Do you build iron farms?",
        "🛡️ Do you use enchanted golden apples?",

        # Pro (34)
        "🛠️ How do you optimize redstone builds?",
        "🛡️ Do you prefer PvP or PvE?",
        "🗺️ How do you speedrun the Ender Dragon?",
        "🐉 Do you respawn the Ender Dragon?",
        "🔥 How do you survive in hardcore mode?",
        "🛤️ Do you build nether highway systems?",
        "🪙 Do you maximize villager trading halls?",
        "🛠️ Do you build mega bases?",
        "🛡️ Do you fight multiple Withers?",
        "🗺️ How do you raid ocean monuments efficiently?",
        "🐠 Do you farm guardians?",
        "🛠️ Do you build gold farms?",
        "🛡️ Do you use TNT dupers?",
        "🗺️ How do you raid bastions safely?",
        "🔥 Do you build blaze farms?",
        "🛠️ Do you build enderman farms?",
        "🛡️ Do you use Elytra for travel?",
        "🗺️ How do you raid woodland mansions?",
        "🐝 Do you automate honey farms?",
        "🛠️ Do you build shulker farms?",
        "🛡️ Do you use tridents in PvP?",
        "🗺️ How do you raid desert temples efficiently?",
        "🐢 Do you automate turtle farms?",
        "🛠️ Do you build kelp farms?",
        "🛡️ Do you use crossbows in PvP?",
        "🗺️ How do you raid igloos?",
        "🐇 Do you automate rabbit farms?",
        "🛠️ Do you build creeper farms?",
        "🛡️ Do you use shields in pro PvP?",
        "🗺️ How do you raid pillager outposts?",
        "🐎 Do you maximize horse breeding?",
        "🛠️ Do you build end gateways?",
        "🛡️ Do you use enchanted gear in tournaments?",
        "🛠️ Do you build multi‑farm complexes?"

    ]
}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

# revive_settings = {
#   guild_id: {
#       "revives": [{"channel": id, "delay": seconds, "category": str}, ...],
#       "custom_categories": {"catname": ["q1","q2",...]}
#   }
# }

# ---------- Persistence ----------
DB_FILE = "revive_settings.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS revives (
            guild_id TEXT,
            channel_id INTEGER,
            delay INTEGER,
            category TEXT,
            role_id INTEGER
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS custom_categories (
            guild_id TEXT,
            name TEXT,
            questions TEXT  -- store as JSON string
        )
        """)
        await db.commit()


async def load_revives(guild_id: int):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute(
            "SELECT channel_id, delay, category, role_id FROM revives WHERE guild_id = ?",
            (str(guild_id),)
        )
        rows = await cursor.fetchall()
        return [
            {"channel": r[0], "delay": r[1], "category": r[2], "role_id": r[3]}
            for r in rows
        ]

async def save_revive(guild_id: int, channel_id: int, delay: int, category: str, role_id: int = None):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT INTO revives VALUES (?, ?, ?, ?, ?)",
            (str(guild_id), channel_id, delay, category, role_id)
        )
        await db.commit()


async def remove_revive(guild_id: int, channel_id: int):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("DELETE FROM revives WHERE guild_id = ? AND channel_id = ?", (str(guild_id), channel_id))
        await db.commit()

async def load_categories(guild_id: int):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT name, questions FROM custom_categories WHERE guild_id = ?", (str(guild_id),))
        rows = await cursor.fetchall()
        return {r[0]: json.loads(r[1]) for r in rows}


# ---------- Events ----------
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    await init_db()  # initialize SQLite tables instead of loading JSON

    guild = discord.Object(id=1413551789034307657)  # dev server ID
    global_cmds = await tree.sync()
    print(f"🌍 Synced {len(global_cmds)} global commands")
    guild_cmds = await tree.sync(guild=guild)
    print(f"⚡ Synced {len(guild_cmds)} commands to guild {guild.id}")

    revive_loop.start()


# ---------- Helpers ----------
def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.manage_guild

async def get_questions(guild_id: int, category: str):
    # Load custom categories from DB
    custom = await load_categories(guild_id)
    builtin = BUILTIN_POOLS.get(category, [])
    return builtin + custom.get(category, [])

async def all_categories(guild_id: int):
    # Load custom categories from DB
    custom = await load_categories(guild_id)
    return list(BUILTIN_POOLS.keys()) + list(custom.keys())

def make_embed(category: str, question: str):
    colors = {
        "general": discord.Color.blurple(),
        "apex": discord.Color.red(),
        "cod": discord.Color.dark_gray(),
        "minecraft": discord.Color.green()
    }
    color = colors.get(category, discord.Color.gold())  # default gold for custom

    embed = Embed(
        title="✨ Revive Time!",
        description=question,
        color=color
    )
    embed.set_footer(text=f"Category: {category.capitalize()} • Stay active!")
    return embed

# ---------- Commands ----------
@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

@tree.command(name="help", description="Show all commands and categories")
async def help_cmd(interaction: discord.Interaction):
  categories = ", ".join(await all_categories(interaction.guild_id))
  await interaction.response.send_message(
        f"📖 **Available Commands:**\n"
        f"- /setup_revive → Add a revive channel (delay + category)\n"
        f"- /remove_revive → Remove revive from a channel\n"
        f"- /add_category → Create a new custom category\n"
        f"- /remove_category → Delete a custom category\n"
        f"- /add_question → Add a question to a category\n"
        f"- /remove_question → Remove a question from a category\n"
        f"- /list_questions → Paginate through all questions in a category\n"
        f"- /revive_now → Trigger a revive instantly (10‑min cooldown per guild)\n"
        f"- /metrics → Show revive counts for this guild\n"
        f"- /bot_status → Full bot status (revives + categories)\n"
        f"- /ping → Check if the bot is alive\n\n"
        f"🎯 **Categories:** {categories}\n\n"
        f"✨ **Notes:** Revive embeds now use category‑specific colors, "
        f"automatic revives are logged and tracked, and deleted channels are cleaned up.",
        ephemeral=True
    )


@tree.command(name="setup_revive", description="Add a revive channel with delay and category")
@app_commands.describe(
    channel="Channel to revive",
    minutes="Delay in minutes",
    category="Category to use",
    role="Optional role to mention when reviving"
)
async def setup_revive(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    minutes: int,
    category: str,
    role: discord.Role = None   # optional
):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return

    if not channel.permissions_for(interaction.guild.me).send_messages:
        await interaction.response.send_message("❌ I cannot send messages in that channel.", ephemeral=True)
        return

    # Check if channel already has a revive setup
    revives = await load_revives(interaction.guild_id)
    if any(s["channel"] == channel.id for s in revives):
        await interaction.response.send_message("❌ This channel already has a revive setup.", ephemeral=True)
        return

    # Save the revive setup in DB (now includes role_id)
    await save_revive(
        interaction.guild_id,
        channel.id,
        minutes * 60,
        category,
        role.id if role else None
    )

    await interaction.response.send_message(
        f"✅ Added revive in {channel.mention}, delay {minutes} minutes, category {category}"
        + (f", role {role.mention}" if role else "") + ".",
        ephemeral=True
    )


# --- Autocomplete for category ---
@setup_revive.autocomplete("category")
async def category_autocomplete(interaction: discord.Interaction, current: str):
    # Load custom categories from DB
    custom = await load_categories(interaction.guild_id)
    # Combine built-in + custom
    cats = list(BUILTIN_POOLS.keys()) + list(custom.keys())
    # Filter by what the user typed
    return [
        app_commands.Choice(name=cat, value=cat)
        for cat in cats if current.lower() in cat.lower()
    ][:25]  # Discord allows max 25 choices

  

@tree.command(name="remove_revive", description="Remove revive from a channel")
@app_commands.describe(channel="Channel that currently has a revive setup")
async def remove_revive(interaction: discord.Interaction, channel: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Convert string ID back to channel object
    ch = interaction.guild.get_channel(int(channel))
    if not ch:
        await interaction.response.send_message("❌ Channel not found.", ephemeral=True)
        return

    # Remove revive from DB
    await remove_revive(interaction.guild_id, ch.id)

    await interaction.response.send_message(f"✅ Revive removed from {ch.mention}.", ephemeral=True)

# --- Autocomplete for remove_revive ---
@remove_revive.autocomplete("channel")
async def remove_revive_autocomplete(interaction: discord.Interaction, current: str):
    # Load revives from DB instead of revive_settings
    revives = await load_revives(interaction.guild_id)
    choices = []
    for s in revives:
        ch = interaction.guild.get_channel(s["channel"])
        if ch and current.lower() in ch.name.lower():
            choices.append(app_commands.Choice(name=ch.name, value=str(ch.id)))
    return choices[:25]

@tree.command(name="add_category", description="Add a new custom category")
async def add_category(interaction: discord.Interaction, name: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Prevent overriding built-in categories
    if name in BUILTIN_POOLS:
        await interaction.response.send_message("❌ Cannot override built-in categories.", ephemeral=True)
        return

    # Save new category in DB
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT INTO custom_categories VALUES (?, ?, ?)",
            (str(interaction.guild_id), name, json.dumps([]))
        )
        await db.commit()

    await interaction.response.send_message(
        f"✅ Custom category '{name}' added.",
        ephemeral=True
    )

@tree.command(name="remove_category", description="Remove a custom category")
async def remove_category(interaction: discord.Interaction, name: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Prevent deleting built-in categories
    if name in BUILTIN_POOLS:
        await interaction.response.send_message("❌ Cannot delete built-in categories.", ephemeral=True)
        return

    # Delete category from DB
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "DELETE FROM custom_categories WHERE guild_id = ? AND name = ?",
            (str(interaction.guild_id), name)
        )
        await db.commit()

    await interaction.response.send_message(
        f"✅ Custom category '{name}' removed.",
        ephemeral=True
    )

# --- Autocomplete for remove_category ---
@remove_category.autocomplete("name")
async def remove_category_autocomplete(interaction: discord.Interaction, current: str):
    # Only show custom categories (not built-ins)
    custom = await load_categories(interaction.guild_id)
    cats = list(custom.keys())
    return [
        app_commands.Choice(name=cat, value=cat)
        for cat in cats if current.lower() in cat.lower()
    ][:25]


@tree.command(name="add_question", description="Add a question to a category")
@app_commands.describe(category="Category to add the question to", question="The question text")
async def add_question(interaction: discord.Interaction, category: str, question: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Load existing questions from DB (custom additions)
    custom = await load_categories(interaction.guild_id)
    questions = custom.get(category, [])
    questions.append(question)

    # Save updated list back to DB
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO custom_categories VALUES (?, ?, ?)",
            (str(interaction.guild_id), category, json.dumps(questions))
        )
        await db.commit()

    await interaction.response.send_message(f"✅ Question added to '{category}'.", ephemeral=True)

# --- Autocomplete for add_question ---
@add_question.autocomplete("category")
async def add_question_autocomplete(interaction: discord.Interaction, current: str):
    custom = await load_categories(interaction.guild_id)
    cats = list(BUILTIN_POOLS.keys()) + list(custom.keys())
    return [
        app_commands.Choice(name=cat, value=cat)
        for cat in cats if current.lower() in cat.lower()
    ][:25]


@tree.command(name="remove_question", description="Remove a question from a category")
@app_commands.describe(category="Category to remove the question from", question="The exact question text")
async def remove_question(interaction: discord.Interaction, category: str, question: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Load existing questions from DB (custom additions)
    custom = await load_categories(interaction.guild_id)
    if category not in custom:
        await interaction.response.send_message("❌ Category not found or no custom additions.", ephemeral=True)
        return

    questions = custom[category]
    if question not in questions:
        await interaction.response.send_message("❌ You can only remove questions you added.", ephemeral=True)
        return

    # Remove from DB additions
    questions.remove(question)
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "UPDATE custom_categories SET questions = ? WHERE guild_id = ? AND name = ?",
            (json.dumps(questions), str(interaction.guild_id), category)
        )
        await db.commit()

    await interaction.response.send_message(f"✅ Custom question removed from '{category}'.", ephemeral=True)

# --- Autocomplete for remove_question ---
@remove_question.autocomplete("category")
async def remove_question_autocomplete(interaction: discord.Interaction, current: str):
    custom = await load_categories(interaction.guild_id)
    cats = list(BUILTIN_POOLS.keys()) + list(custom.keys())
    return [
        app_commands.Choice(name=cat, value=cat)
        for cat in cats if current.lower() in cat.lower()
    ][:25]



@tree.command(name="bot_status", description="Show full bot status")
async def bot_status(interaction: discord.Interaction):
    embed = Embed(title="🤖 Bot Status", color=discord.Color.gold())

    # Revives
    revives = await load_revives(interaction.guild_id)
    if revives:
        revives_text = ""
        for s in revives:
            channel = interaction.guild.get_channel(s["channel"])
            delay_min = s["delay"] // 60
            if channel:
                revives_text += f"{channel.mention} | {delay_min} min | {s['category']}\n"
            else:
                revives_text += f"⚠️ Channel deleted | {delay_min} min | {s['category']}\n"
        embed.add_field(name="Revive Channels", value=revives_text, inline=False)
    else:
        embed.add_field(name="Revive Channels", value="None", inline=False)

    # Categories
    custom = await load_categories(interaction.guild_id)
    cats_text = ""
    for cat in list(BUILTIN_POOLS.keys()) + list(custom.keys()):
        builtin_count = len(BUILTIN_POOLS.get(cat, []))
        custom_count = len(custom.get(cat, []))
        cats_text += f"**{cat}** → {custom_count} custom, {builtin_count} built-in\n"
    embed.add_field(name="Categories", value=cats_text, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="metrics", description="Show revive metrics for this guild")
async def metrics(interaction: discord.Interaction):
    count = metrics_data.get(interaction.guild_id, 0)
    await interaction.response.send_message(
        f"📊 Revives fired in this guild: {count}",
        ephemeral=True
    )


@tree.command(name="revive_now", description="Trigger a revive message instantly")
async def revive_now(interaction: discord.Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Cooldown check (10 minutes per guild)
    now = time.time()
    last = revive_cooldowns.get(interaction.guild_id, 0)
    if now - last < 600:
        await interaction.response.send_message("❌ Cooldown active, try again later.", ephemeral=True)
        return
    revive_cooldowns[interaction.guild_id] = now

    revives = await load_revives(interaction.guild_id)
    if not revives:
        await interaction.response.send_message("❌ No revive channels set.", ephemeral=True)
        return

    for settings in revives:
        channel = interaction.guild.get_channel(settings["channel"])
        if channel:
            questions = await get_questions(interaction.guild_id, settings["category"])
            if questions:
                question = random.choice(questions)
                await channel.send(embed=make_embed(settings["category"], question))

                metrics_data[interaction.guild_id] = metrics_data.get(interaction.guild_id, 0) + 1
                print(f"[Revive] {interaction.guild.name} → {channel.name} | {settings['category']}")

    await interaction.response.send_message("✅ Revive triggered in all configured channels.", ephemeral=True)

              
# --- Pagination View ---
class QuestionPagination(View):
    def __init__(self, questions, category, page=1, per_page=20):
        super().__init__(timeout=60)  # disables buttons after 60s
        self.questions = questions
        self.category = category
        self.page = page
        self.per_page = per_page
        self.total_pages = (len(questions) + per_page - 1) // per_page

    def build_embed(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        page_questions = self.questions[start:end]

        embed = Embed(title=f"📋 Questions in '{self.category}'", color=discord.Color.gold())
        embed.description = "\n".join(f"{i}. {q}" for i, q in enumerate(page_questions, start=start + 1))
        embed.set_footer(text=f"Page {self.page}/{self.total_pages} • {len(self.questions)} total questions")
        return embed

    @button(label="⬅️ Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @button(label="➡️ Next", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.total_pages:
            self.page += 1
            await interaction.response.edit_message(embed=self.build_embed(), view=self)

@tree.command(name="list_questions", description="List all questions in a category with pagination")
@app_commands.describe(category="Category to list questions from")
async def list_questions(interaction: discord.Interaction, category: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    custom = (await load_categories(interaction.guild_id)).get(category, [])
    builtin = BUILTIN_POOLS.get(category, [])
    questions = custom + builtin

    if not questions:
        await interaction.response.send_message("❌ No questions found in that category.", ephemeral=True)
        return

    view = QuestionPagination(questions, category)
    await interaction.response.send_message(embed=view.build_embed(), view=view, ephemeral=True)


@list_questions.autocomplete("category")
async def list_questions_autocomplete(interaction: discord.Interaction, current: str):
    cats = await all_categories(interaction.guild_id)
    return [
        app_commands.Choice(name=cat, value=cat)
        for cat in cats if current.lower() in cat.lower()
    ][:25]



   
# ---------- Background Loop ----------
@tasks.loop(minutes=5)
async def revive_loop():
    for guild in client.guilds:
        revives = await load_revives(guild.id)
        for settings in revives:
            channel = guild.get_channel(settings["channel"])
            delay = settings.get("delay", 7200)
            if channel:
                try:
                    async for message in channel.history(limit=1):
                        if (discord.utils.utcnow() - message.created_at).total_seconds() > delay:
                            questions = await get_questions(guild.id, settings["category"])
                            if questions:
                                question = random.choice(questions)

                                # 🔑 NEW: check for role_id
                                role = guild.get_role(settings.get("role_id")) if settings.get("role_id") else None
                                content = role.mention if role else None

                                await channel.send(content=content, embed=make_embed(settings["category"], question))

                                metrics_data[guild.id] = metrics_data.get(guild.id, 0) + 1
                                print(f"[Revive] {guild.name} → {channel.name} | {settings['category']}"
                                      + (f" | Role: {role.name}" if role else ""))
                except Exception as e:
                    print(f"⚠️ Could not check {channel}: {e}")
            else:
                # Cleanup for deleted channels
                await remove_revive(guild.id, settings["channel"])
                print(f"⚠️ Removed revive entry for deleted channel in {guild.name}")

# ---------- Run ----------
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN environment variable not set!")
client.run(token)


