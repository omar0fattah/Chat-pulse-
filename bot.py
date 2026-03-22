import os
import discord
from discord.ext import tasks

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Create client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    revive_channels.start()  # start the loop only after bot is ready

@tasks.loop(minutes=30)
async def revive_channels():
    for guild in client.guilds:
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=1):
                    # If last message older than 2 hours, send revive
                    if (discord.utils.utcnow() - message.created_at).total_seconds() > 7200:
                        await channel.send("👋 Anyone still alive here?")
            except Exception as e:
                print(f"⚠️ Could not check {channel}: {e}")

# Run bot with token from Railway environment variable
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("❌ DISCORD_TOKEN environment variable not set!")
client.run(token)
