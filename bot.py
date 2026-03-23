import os
import random
import json
import discord
from discord import app_commands
from discord.ext import tasks, commands

SETTINGS_FILE = "revive_settings.json"

# Question pools by category
QUESTION_POOLS = {
    "general": [
        "👀 What’s everyone up to today?",
        "🔥 Share the last song you listened to!",
        "💡 What’s a random fun fact you know?",
        "🍕 Pineapple on pizza: yes or no?",
        "🎮 What game are you playing lately?"
    ],
    "apex": [
        "🏹 Who’s your main legend?",
        "💥 Favorite weapon loadout?",
        "🗺️ Best drop spot this season?",
        "🔥 Ranked grind or casual vibes?"
    ],
    "cod": [
        "🔫 What’s your go-to class setup?",
        "🎯 Sniping or rushing?",
        "💣 Favorite map of all time?",
        "⚔️ Zombies or Multiplayer?"
    ],
    "minecraft": [
        "⛏️ What’s your latest build?",
        "🌍 Survival or Creative?",
        "🐉 Ever beaten the Ender Dragon?",
        "🏠 Show off your base design!"
    ]
}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

# Store revive settings per guild
# {guild_id: [{"channel": channel_id, "delay": seconds, "category": str}, ...]}
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

# ---------- Commands ----------
@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

@tree.command(name="help", description="Show all commands and categories")
async def help_cmd(interaction: discord.Interaction):
    categories = ", ".join(QUESTION_POOLS.keys())
    await interaction.response.send_message(
        f"📖 **Available Commands:**\n"
        f"- /setup_revive (add channel, delay, category)\n"
        f"- /remove_revive (remove channel)\n"
        f"- /setup_delay (update delay)\n"
        f"- /revive_now (manual trigger)\n"
        f"- /show_revive_settings (view config)\n"
        f"- /ping (check bot)\n\n"
        f"🎯 **Categories:** {categories}",
        ephemeral=True
    )

@tree.command(name="setup_revive", description="Add a revive channel with delay and category")
@app_commands.describe(channel="Channel to revive", minutes="Delay in minutes", category="Pick a category")
@app_commands.choices(category=[
    app_commands.Choice(name="General", value="general"),
    app_commands.Choice(name="Apex Legends", value="apex"),
    app_commands.Choice(name="Call of Duty", value="cod"),
    app_commands.Choice(name="Minecraft", value="minecraft"),
])
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel, minutes: int = 120, category: app_commands.Choice[str] = None):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return

    chosen_category = category.value if category else "general"
    guild_settings = revive_settings.get(str(interaction.guild_id), [])
    guild_settings.append({"channel": channel.id, "delay": minutes * 60, "category": chosen_category})
    revive_settings[str(interaction.guild_id)] = guild_settings
    save_settings()

    await interaction.response.send_message(
        f"✅ Added revive in {channel.mention}, delay {minutes} minutes, category {chosen_category}.",
        ephemeral=True
    )

@tree.command(name="remove_revive", description="Remove revive from a channel")
async def remove_revive(interaction: discord.Interaction, channel: discord.TextChannel):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    guild_settings = revive_settings.get(str(interaction.guild_id), [])
    new_settings = [s for s in guild_settings if s["channel"] != channel.id]
    revive_settings[str(interaction.guild_id)] = new_settings
    save_settings()

    await interaction.response.send_message(f"✅ Revive removed from {channel.mention}.", ephemeral=True)

@tree.command(name="setup_delay", description="Set inactivity delay before revive (in minutes)")
async def setup_delay(interaction: discord.Interaction, minutes: int):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return

    guild_settings = revive_settings.get(str(interaction.guild_id), [])
    for s in guild_settings:
        s["delay"] = minutes * 60
    revive_settings[str(interaction.guild_id)] = guild_settings
    save_settings()

    await interaction.response.send_message(f"✅ Revive delay updated to {minutes} minutes.", ephemeral=True)

@tree.command(name="show_revive_settings", description="View revive settings for this server")
async def show_revive_settings(interaction: discord.Interaction):
    guild_settings = revive_settings.get(str(interaction.guild_id), [])
    if not guild_settings:
        await interaction.response.send_message("❌ No revive channels set.", ephemeral=True)
        return

    msg = "📊 **Revive Settings:**\n"
    for s in guild_settings:
        channel = interaction.guild.get_channel(s["channel"])
        delay_min = s["delay"] // 60
        msg += f"- {channel.mention if channel else 'Unknown'} | Delay: {delay_min} min | Category: {s['category']}\n"

    await interaction.response.send_message(msg, ephemeral=True)

@tree.command(name="revive_now", description="Trigger a revive message instantly")
@app_commands.checks.cooldown(1, 60.0)  # 1 use per minute per guild
async def revive_now(interaction: discord.Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

    guild_settings = revive_settings.get(str(interaction.guild_id), [])
    if not guild_settings:
        await interaction.response.send_message("❌ No revive channels set.", ephemeral=True)
        return

    for settings in guild_settings:
        channel = interaction.guild.get_channel(settings["channel"])
        if channel:
            category = settings.get("category", "general")
            questions = QUESTION_POOLS.get(category, QUESTION_POOLS["general"])
            await channel.send(random.choice(questions))

    await interaction.response.send_message("✅ Revive triggered in all configured channels.", ephemeral=True)

# ---------- Background Loop ----------
@tasks.loop(minutes=5)
async def revive_loop():
    for guild in client.guilds:
        guild_settings = revive_settings.get(str(guild.id), [])
        for settings in guild_settings:
            channel = guild.get_channel(settings.get("channel"))
            delay = settings.get("delay", 7200)
            if channel:
                try:
                    async for message in channel.history(limit=1):
                        if (discord.utils.utcnow() - message.created_at).total_seconds() > delay:
                            category = settings.get("category", "general")
                            questions = QUESTION_POOLS.get(category, QUESTION_POOLS["general"])
                            await channel.send(random.choice(questions))
                except Exception as e:
                    print(f"⚠️ Could not check {channel}: {e}")

# ---------- Run ----------
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DIS
