import os
import random
import json
import discord
from discord import app_commands, Embed
from discord.ext import tasks, commands

SETTINGS_FILE = "revive_settings.json"

# Built-in question pools (locked, cannot be deleted)
BUILTIN_POOLS = {
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
    embed = Embed(
        title="✨ Revive Time!",
        description=question,
        color=discord.Color.blurple()
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
        f"- /setup_revive (add channel, delay, category)\n"
        f"- /remove_revive (remove channel)\n"
        f"- /add_category (create new category)\n"
        f"- /remove_category (delete custom category)\n"
        f"- /add_question (add question to category)\n"
        f"- /remove_question (remove question from category)\n"
        f"- /revive_now (manual trigger)\n"
        f"- /show_revive_settings (view revive channels)\n"
        f"- /bot_status (full bot status)\n"
        f"- /ping (check bot)\n\n"
        f"🎯 **Categories:** {categories}",
        ephemeral=True
    )

@tree.command(name="setup_revive", description="Add a revive channel with delay and category")
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel, minutes: int = 120, category: str = "general"):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return
    if category not in all_categories(interaction.guild_id):
        await interaction.response.send_message(f"❌ Invalid category. Choose from: {', '.join(all_categories(interaction.guild_id))}", ephemeral=True)
        return

    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
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

@tree.command(name="show_revive_settings", description="View revive settings for this server")
async def show_revive_settings(interaction: discord.Interaction):
    guild_data = revive_settings.get(str(interaction.guild_id), {"revives": [], "custom_categories": {}})
    if not guild_data["revives"]:
        await interaction.response.send_message("❌ No revive channels set.", ephemeral=True)
        return

    msg = "📊 **Revive Settings:**\n"
    for s in guild_data["revives"]:
        channel = interaction.guild.get_channel(s["channel"])
        delay_min = s["delay"] // 60
        msg += f"- {channel.mention if channel else 'Unknown'} | Delay: {delay_min} min | Category: {s['category']}\n"

    await interaction.response.send_message(msg, ephemeral=True)

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
            revives_text += f"{channel.mention if channel else 'Unknown'} | {delay_min} min | {s['category']}\n"
        embed.add_field(name="Revive Channels", value=revives_text, inline=False)
    else:
        embed.add_field(name="Revive Channels", value="None", inline=False)

    # Categories
    cats_text = ""
    for cat in all_categories(interaction.guild_id):
        questions = get_questions(interaction.guild_id, cat)
        cats_text += f"**{cat}** ({len(questions)} questions)\n"
    embed.add_field(name="Categories", value=cats_text, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="revive_now", description="Trigger a revive message instantly")
async def revive_now(interaction: discord.Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("❌ You need Manage Server permission.", ephemeral=True)
        return

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

    await interaction.response.send_message("✅ Revive triggered in all configured channels.", ephemeral=True)

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
                except Exception as e:
                    print(f"⚠️ Could not check {channel}: {e}")

# ---------- Run ----------
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN environment variable not set!")
client.run(token)


