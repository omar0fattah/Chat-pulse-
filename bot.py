import os
import random
import discord
from discord import app_commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Store revive settings per guild
revive_settings = {}  # {guild_id: {"channel": channel_id, "delay": seconds}}

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    guild = discord.Object(id=1413551789034307657)  # your server ID

    # Sync globally (slow propagation, but needed for all servers)
    global_cmds = await tree.sync()
    print(f"🌍 Synced {len(global_cmds)} global commands")

    # Sync instantly to your dev guild
    guild_cmds = await tree.sync(guild=guild)
    print(f"⚡ Synced {len(guild_cmds)} commands to guild {guild.id}")

    revive_loop.start()


@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

@tree.command(name="setup_revive", description="Choose a channel and delay for revive messages")
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel, minutes: int = 120):
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return
    revive_settings[interaction.guild_id] = {"channel": channel.id, "delay": minutes * 60}
    await interaction.response.send_message(
        f"✅ Revive channel set to {channel.mention} with {minutes} minutes delay.", ephemeral=True
    )

@tree.command(name="setup_delay", description="Set inactivity delay before revive (in minutes)")
async def setup_delay(interaction: discord.Interaction, minutes: int):
    if minutes < 1:
        await interaction.response.send_message("❌ Delay must be at least 1 minute.", ephemeral=True)
        return
    settings = revive_settings.get(interaction.guild_id, {})
    settings["delay"] = minutes * 60
    revive_settings[interaction.guild_id] = settings
    await interaction.response.send_message(
        f"✅ Revive delay updated to {minutes} minutes.", ephemeral=True
    )

@tree.command(name="revive_now", description="Trigger a revive message instantly")
async def revive_now(interaction: discord.Interaction):
    settings = revive_settings.get(interaction.guild_id)
    if not settings or "channel" not in settings:
        await interaction.response.send_message("❌ No revive channel set yet.", ephemeral=True)
        return
    channel = interaction.guild.get_channel(settings["channel"])
    if not channel:
        await interaction.response.send_message("❌ Revive channel not found.", ephemeral=True)
        return
    questions = [
        "👀 What’s everyone up to today?",
        "🔥 Share the last song you listened to!",
        "💡 What’s a random fun fact you know?",
        "🍕 Pineapple on pizza: yes or no?",
        "🎮 What game are you playing lately?"
    ]
    await channel.send(random.choice(questions))
    await interaction.response.send_message(f"✅ Revive triggered in {channel.mention}", ephemeral=True)

@tasks.loop(minutes=5)
async def revive_loop():
    for guild in client.guilds:
        settings = revive_settings.get(guild.id)
        if not settings:
            continue
        channel = guild.get_channel(settings.get("channel"))
        delay = settings.get("delay", 7200)
        if channel:
            try:
                async for message in channel.history(limit=1):
                    if (discord.utils.utcnow() - message.created_at).total_seconds() > delay:
                        questions = [
                            "👀 What’s everyone up to today?",
                            "🔥 Share the last song you listened to!",
                            "💡 What’s a random fun fact you know?",
                            "🍕 Pineapple on pizza: yes or no?",
                            "🎮 What game are you playing lately?"
                        ]
                        await channel.send(random.choice(questions))
            except Exception as e:
                print(f"⚠️ Could not check {channel}: {e}")

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN environment variable not set!")
client.run(token)
