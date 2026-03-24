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


