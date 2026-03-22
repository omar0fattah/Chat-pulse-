import os
import discord
from discord.ext import tasks

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    revive_channels.start()  # start the loop here

@tasks.loop(minutes=30)
async def revive_channels():
    for guild in client.guilds:
        for channel in guild.text_channels:
            async for message in channel.history(limit=1):
                if (discord.utils.utcnow() - message.created_at).total_seconds() > 7200:
                    await channel.send("👋 Anyone still alive here?")

client.run(os.getenv("DISCORD_TOKEN"))
