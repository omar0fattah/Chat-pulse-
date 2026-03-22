import os
import discord
from discord import app_commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Store revive channel IDs per guild
revive_channels_map = {}

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    # Sync slash commands with Discord
    await tree.sync()
    revive_loop.start()

# /ping command
@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

# /setup_revive command
@tree.command(name="setup_revive", description="Choose a channel for revive messages")
async def setup_revive(interaction: discord.Interaction, channel: discord.TextChannel):
    revive_channels_map[interaction.guild_id] = channel.id
    await interaction.response.send_message(
        f"✅ Revive channel set to {channel.mention}", ephemeral=True
    )

# Background revive loop
@tasks.loop(minutes=30)
async def revive_loop():
    for guild in client.guilds:
        channel_id = revive_channels_map.get(guild.id)
        if channel_id:
            channel = guild.get_channel(channel_id)
            if channel:
                try:
                    async for message in channel.history(limit=1):
                        if (discord.utils.utcnow() - message.created_at).total_seconds() > 7200:
                            # Prebuilt revive questions
                            questions = [
                                "👀 What’s everyone up to today?",
                                "🔥 Share the last song you listened to!",
                                "💡 What’s a random fun fact you know?",
                                "🍕 Pineapple on pizza: yes or no?",
                                "🎮 What game are you playing lately?"
                            ]
                            await channel.send(discord.utils.choice(questions))
                except Exception as e:
                    print(f"⚠️ Could not check {channel}: {e}")

# Run bot
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN environment variable not set!")
client.run(token)
