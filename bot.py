import os
import random
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
        "📱 Do you prefer likes or comments?",
        "📱 Do you prefer followers or friends?",
        "📱 Do you prefer private or public accounts?",
        "📱 Do you prefer notifications on or off?",
        "📱 Do you prefer dark mode or light mode?",
        "📱 Do you prefer Android or iOS?",
        "📱 Do you prefer Windows or Mac?",
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
        "💡 What’s a random fun fact you know?",
        "🍕 Pineapple on pizza: yes or no?",
        "🎮 What game are you playing lately?"
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
revive_settings = {}

# ---------- Persistence ----------
def load_settings():
    global revive_settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            revive_settings = json.load(f)
    else:
        revive_settings = {}

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(revive_settings, f, indent=2)

# ---------- Events ----------
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    load_settings()

    guild = discord.Object(id=1413551789034307657)  # dev server ID
    global_cmds = await tree.sync()
    print(f"🌍 Synced {len(global_cmds)} global commands")
    guild_cmds = await tree.sync(guild=guild)
    print(f"⚡ Synced {len(guild_cmds)} commands to guild {guild.id}")

    revive_loop.start()

# ---------- Helpers ----------
def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.manage_guild

def get_questions(guild_id: int, category: str):
    guild_data = revive_settings.get(str(guild_id), {})
    custom = guild_data.get("custom_categories", {})
    if category in BUILTIN_POOLS:
        return BUILTIN_POOLS[category]
    return custom.get(category, [])

def all_categories(guild_id: int):
    guild_data = revive_settings.get(str(guild_id), {})
    custom = guild_data.get("custom_categories", {})
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
    categories = ", ".join(all_categories(interaction.guild_id))
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
async def setup_revive(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    minutes: int = 120,
    category: str = "general"
):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return

    # --- Stage 4: Permission validation ---
    if not channel.permissions_for(interaction.guild.me).send_messages:
        await interaction.response.send_message("❌ I cannot send messages in that channel.", ephemeral=True)
        return

    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    # Prevent duplicate revive setups for the same channel
    for s in guild_data["revives"]:
        if s["channel"] == channel.id:
            await interaction.response.send_message("❌ This channel already has a revive setup.", ephemeral=True)
            return

    guild_data["revives"].append({"channel": channel.id, "delay": minutes * 60, "category": category})
    revive_settings[str(interaction.guild_id)] = guild_data
    save_settings()

    await interaction.response.send_message(
        f"✅ Added revive in {channel.mention}, delay {minutes} minutes, category {category}.",
        ephemeral=True
    )


@tree.command(name="remove_revive", description="Remove revive from a channel")
async def remove_revive(interaction: discord.Interaction, channel: discord.TextChannel):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    guild_data["revives"] = [s for s in guild_data["revives"] if s["channel"] != channel.id]
    revive_settings[str(interaction.guild_id)] = guild_data
    save_settings()

    await interaction.response.send_message(f"✅ Revive removed from {channel.mention}.", ephemeral=True)

@tree.command(name="add_category", description="Add a new custom category")
async def add_category(interaction: discord.Interaction, name: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    if name in BUILTIN_POOLS:
        await interaction.response.send_message("❌ Cannot override built-in categories.", ephemeral=True)
        return
    guild_data["custom_categories"].setdefault(name, [])
    revive_settings[str(interaction.guild_id)] = guild_data
    save_settings()
    await interaction.response.send_message(f"✅ Custom category '{name}' added.", ephemeral=True)

@tree.command(name="remove_category", description="Remove a custom category")
async def remove_category(interaction: discord.Interaction, name: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    if name in BUILTIN_POOLS:
        await interaction.response.send_message("❌ Cannot delete built-in categories.", ephemeral=True)
        return
    if name in guild_data["custom_categories"]:
        del guild_data["custom_categories"][name]
        revive_settings[str(interaction.guild_id)] = guild_data
        save_settings()
        await interaction.response.send_message(f"✅ Custom category '{name}' removed.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Category not found.", ephemeral=True)

@tree.command(name="add_question", description="Add a question to a category")
async def add_question(interaction: discord.Interaction, category: str, question: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if category in BUILTIN_POOLS:
        await interaction.response.send_message("❌ Cannot add questions to built-in categories.", ephemeral=True)
        return
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    if category not in guild_data["custom_categories"]:
        await interaction.response.send_message("❌ Category not found.", ephemeral=True)
        return
    guild_data["custom_categories"][category].append(question)
    revive_settings[str(interaction.guild_id)] = guild_data
    save_settings()
    await interaction.response.send_message(f"✅ Question added to '{category}'.", ephemeral=True)

@tree.command(name="remove_question", description="Remove a question from a category")
async def remove_question(interaction: discord.Interaction, category: str, question: str):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if category in BUILTIN_POOLS:
        await interaction.response.send_message("❌ Cannot remove questions from built-in categories.", ephemeral=True)
        return
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    if category not in guild_data["custom_categories"]:
        await interaction.response.send_message("❌ Category not found.", ephemeral=True)
        return
    if question not in guild_data["custom_categories"][category]:
        await interaction.response.send_message("❌ Question not found in that category.", ephemeral=True)
        return
    guild_data["custom_categories"][category].remove(question)
    revive_settings[str(interaction.guild_id)] = guild_data
    save_settings()
    await interaction.response.send_message(f"✅ Question removed from '{category}'.", ephemeral=True)

@tree.command(name="bot_status", description="Show full bot status")
async def bot_status(interaction: discord.Interaction):
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    embed = Embed(title="🤖 Bot Status", color=discord.Color.gold())

    # Revives
    if guild_data["revives"]:
        revives_text = ""
        for s in guild_data["revives"]:
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
    cats_text = ""
    for cat in all_categories(interaction.guild_id):
        builtin_count = len(BUILTIN_POOLS.get(cat, []))
        custom_count = len(
            revive_settings.get(str(interaction.guild_id), {})
            .get("custom_categories", {})
            .get(cat, [])
        )
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

    # --- Stage 4: Cooldown check (10 minutes per guild) ---
    now = time.time()
    last = revive_cooldowns.get(interaction.guild_id, 0)
    if now - last < 600:  # 600 seconds = 10 minutes
        await interaction.response.send_message("❌ Cooldown active, try again later.", ephemeral=True)
        return
    revive_cooldowns[interaction.guild_id] = now

    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    if not guild_data["revives"]:
        await interaction.response.send_message("❌ No revive channels set.", ephemeral=True)
        return

    for settings in guild_data["revives"]:
        channel = interaction.guild.get_channel(settings["channel"])
        if channel:
            questions = get_questions(interaction.guild_id, settings["category"])
            if questions:
                question = random.choice(questions)
                await channel.send(embed=make_embed(settings["category"], question))

                # --- Section 5: Metrics + Logging ---
                metrics_data[interaction.guild_id] = metrics_data.get(interaction.guild_id, 0) + 1
                print(f"[Revive] {interaction.guild.name} → {channel.name} | {settings['category']}")

    await interaction.response.send_message("✅ Revive triggered in all configured channels.", ephemeral=True)

@tree.command(name="list_questions", description="List all questions in a category with pagination")
async def list_questions(
    interaction: discord.Interaction,
    category: str,
    page: int = 1
):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    # Get questions (custom first, then built-in)
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    custom = guild_data.get("custom_categories", {}).get(category, [])
    builtin = BUILTIN_POOLS.get(category, [])
    questions = custom + builtin

    if not questions:
        await interaction.response.send_message("❌ No questions found in that category.", ephemeral=True)
        return

    # Pagination (20 per page)
    per_page = 20
    total_pages = (len(questions) + per_page - 1) // per_page
    if page < 1 or page > total_pages:
        await interaction.response.send_message(f"❌ Invalid page. Choose 1–{total_pages}.", ephemeral=True)
        return

    start = (page - 1) * per_page
    end = start + per_page
    page_questions = questions[start:end]

    # Build embed
    embed = Embed(
        title=f"📋 Questions in '{category}'",
        color=discord.Color.gold()
    )
    desc = ""
    for i, q in enumerate(page_questions, start=start + 1):
        desc += f"{i}. {q}\n"
    embed.description = desc
    embed.set_footer(text=f"Page {page}/{total_pages} • {len(questions)} total questions")

    await interaction.response.send_message(embed=embed, ephemeral=True)

   
# ---------- Background Loop ----------
@tasks.loop(minutes=5)
async def revive_loop():
    for guild in client.guilds:
        guild_data = revive_settings.get(str(guild.id), {"revives": [], "custom_categories": {}})
        for settings in guild_data["revives"]:
            channel = guild.get_channel(settings.get("channel"))
            delay = settings.get("delay", 7200)
            if channel:
                try:
                    async for message in channel.history(limit=1):
                        if (discord.utils.utcnow() - message.created_at).total_seconds() > delay:
                            questions = get_questions(guild.id, settings["category"])
                            if questions:
                                question = random.choice(questions)
                                await channel.send(embed=make_embed(settings["category"], question))

                                # --- Section 5: Metrics + Logging ---
                                metrics_data[guild.id] = metrics_data.get(guild.id, 0) + 1
                                print(f"[Revive] {guild.name} → {channel.name} | {settings['category']}")
                except Exception as e:
                    print(f"⚠️ Could not check {channel}: {e}")
            else:
                # --- Stage 4: Cleanup for deleted channels ---
                guild_data["revives"].remove(settings)
                revive_settings[str(guild.id)] = guild_data
                save_settings()
                print(f"⚠️ Removed revive entry for deleted channel in {guild.name}")

# ---------- Run ----------
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN environment variable not set!")
client.run(token)


