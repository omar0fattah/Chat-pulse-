import discord
from discord import app_commands
import asyncio
import random
import os
from datetime import datetime, timedelta

# Get token from environment variable
TOKEN = os.environ.get('TOKEN')

# ============= QUESTION CATEGORIES =============

QUESTIONS = {
    "apex": [
        "Who's your main in Apex and why? 🔫",
        "Hot take: Which legend is actually overrated?",
        "What's the dumbest way you've died in Apex? 💀",
        "Kraber or Mastiff? GO!",
        "Which POI is your drop spot?",
        "Controller or MnK?",
        "Favorite weapon loadout right now?",
        "Which legend needs a buff most?",
        "What's your record kill game? 📊",
        "Who has the best voice lines? 🗣️"
    ],
    "minecraft": [
        "Wooden sword or stone pickaxe first? ⚔️",
        "What's your go-to biome to build in?",
        "Creeper or skeleton - which is more annoying? 💀",
        "Do you dig straight down? (be honest)",
        "Favorite Minecraft memory?",
        "Build battle: Modern house or medieval castle?",
        "Which mob should be added next?",
        "Redstone genius or just a lever puller? 🔴",
        "What's the first thing you do in a new world?",
        "Diamonds - what do you craft first? 💎"
    ],
    "cod": [
        "Favorite COD game of all time? 🎮",
        "SMG or Assault Rifle?",
        "Hardpoint or Search & Destroy?",
        "Most annoying killstreak?",
        "What's your go-to loadout? 🔫",
        "Camping or rushing?",
        "Best map in COD history?",
        "Controller or MnK on COD?",
        "What's your KD ratio? (no judging)",
        "Which OP weapon needs a nerf?"
    ],
    "general": [
        "If you could have dinner with any fictional character, who? 🍕",
        "What's the weirdest food combination you actually enjoy?",
        "If you woke up with a superpower tomorrow, what would it be? ⚡",
        "What movie can you watch over and over? 🎬",
        "If you could instantly master any skill, what?",
        "What's the most useless talent you have?",
        "If animals could talk, which would be the rudest? 🦁",
        "What's a song that always puts you in a good mood? 🎵",
        "If you had to eat one food forever, what?",
        "What's the best advice you've ever received?"
    ],
    "random": [
        "What's the most random fact you know? 🤓",
        "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
        "What's the first thing you'd buy after winning the lottery? 💰",
        "If you could time travel, past or future?",
        "What's your go-to karaoke song? 🎤",
        "Most embarrassing memory from school?",
        "If you were a YouTuber, what content? 📹",
        "What's a smell that brings back memories?",
        "Would you want to know the date of your death?",
        "If you could delete one thing from the internet, what? 🌐"
    ]
}

# Default category (for servers that don't set one)
DEFAULT_CATEGORY = "general"

class CategoryView(discord.ui.View):
    def __init__(self, guild_id, bot):
        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.bot = bot
        
    @discord.ui.select(
        placeholder="Choose a category...",
        options=[
            discord.SelectOption(label="Apex Legends", value="apex", emoji="🔫"),
            discord.SelectOption(label="Minecraft", value="minecraft", emoji="⛏️"),
            discord.SelectOption(label="Call of Duty", value="cod", emoji="💣"),
            discord.SelectOption(label="General Life", value="general", emoji="🌍"),
            discord.SelectOption(label="Random Fun", value="random", emoji="🎲"),
        ]
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.guild_id != self.guild_id:
            await interaction.response.send_message("❌ This menu isn't for your server!", ephemeral=True)
            return
            
        category = select.values[0]
        
        # Save to server settings
        async with self.bot.settings_lock:
            if self.guild_id not in self.bot.server_settings:
                self.bot.server_settings[self.guild_id] = {}
            self.bot.server_settings[self.guild_id]['category'] = category
            
        await interaction.response.send_message(f"✅ Category set to **{select.values[0].title()}**! Now use `/setup` to choose a channel.", ephemeral=True)
        self.stop()

class ChatPulseBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.check_interval = 60
        self.server_settings = {}  # guild_id: {'channel_id': int, 'category': str, 'last_msg': datetime}
        self.settings_lock = asyncio.Lock()

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Slash commands synced")

    async def on_ready(self):
        print(f'✅ Chat Pulse has connected to Discord!')
        print(f'📊 Bot is in {len(self.guilds)} server(s)')
        
        # Initialize settings for each guild
        for guild in self.guilds:
            if guild.id not in self.server_settings:
                self.server_settings[guild.id] = {
                    'channel_id': None,
                    'category': DEFAULT_CATEGORY,
                    'last_msg': {}
                }
        
        # Start the inactivity checker
        self.bg_task = self.loop.create_task(self.check_inactivity())
        print(f'⏰ Inactivity checker started')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Track messages in monitored channels
        if message.guild and message.guild.id in self.server_settings:
            settings = self.server_settings[message.guild.id]
            if settings['channel_id'] == message.channel.id:
                settings['last_msg'][message.channel.id] = datetime.now()

    async def check_inactivity(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                for guild_id, settings in self.server_settings.items():
                    if settings['channel_id']:
                        channel = self.get_channel(settings['channel_id'])
                        if channel:
                            # Initialize if needed
                            if channel.id not in settings['last_msg']:
                                settings['last_msg'][channel.id] = datetime.now()
                            
                            # Check inactivity (2 hours default)
                            time_since = datetime.now() - settings['last_msg'][channel.id]
                            if time_since >= timedelta(hours=2):
                                # Get question from selected category
                                category = settings.get('category', DEFAULT_CATEGORY)
                                questions = QUESTIONS.get(category, QUESTIONS[DEFAULT_CATEGORY])
                                question = random.choice(questions)
                                
                                await channel.send(
                                    f"🌱 **Chat's been quiet for 2 hours!**\n"
                                    f"*{category.title()} question:* {question}"
                                )
                                print(f"📤 Sent {category} revive in guild {guild_id}")
                                settings['last_msg'][channel.id] = datetime.now()
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(self.check_interval)

bot = ChatPulseBot()

# ============= SLASH COMMANDS =============

@bot.tree.command(name="category", description="Choose a question category for your server")
async def category(interaction: discord.Interaction):
    """Open category selection menu"""
    view = CategoryView(interaction.guild_id, bot)
    await interaction.response.send_message("📋 **Select a category:**", view=view, ephemeral=True)

@bot.tree.command(name="setup", description="Set the channel for Chat Pulse")
@app_commands.describe(channel="The channel to revive")
async def setup(interaction: discord.Interaction, channel: discord.TextChannel):
    """Set up the revive channel"""
    async with bot.settings_lock:
        if interaction.guild_id not in bot.server_settings:
            bot.server_settings[interaction.guild_id] = {
                'channel_id': None,
                'category': DEFAULT_CATEGORY,
                'last_msg': {}
            }
        bot.server_settings[interaction.guild_id]['channel_id'] = channel.id
        bot.server_settings[interaction.guild_id]['last_msg'][channel.id] = datetime.now()
    
    await interaction.response.send_message(
        f"✅ **Chat Pulse setup complete!**\n"
        f"📌 Channel: {channel.mention}\n"
        f"🗂️ Current category: {bot.server_settings[interaction.guild_id].get('category', 'general').title()}\n"
        f"💡 Use `/category` to change categories!"
    )

@bot.tree.command(name="status", description="Check chat activity")
async def status(interaction: discord.Interaction):
    """Check current status"""
    settings = bot.server_settings.get(interaction.guild_id)
    
    if not settings or not settings['channel_id']:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.")
        return
    
    channel = bot.get_channel(settings['channel_id'])
    if not channel:
        await interaction.response.send_message("❌ Configured channel not found!")
        return
    
    last_time = settings['last_msg'].get(channel.id, datetime.now())
    time_since = datetime.now() - last_time
    hours = int(time_since.total_seconds() / 3600)
    minutes = int((time_since.total_seconds() / 60) % 60)
    
    await interaction.response.send_message(
        f"📊 **Chat Pulse Status**\n"
        f"📌 Channel: {channel.mention}\n"
        f"🗂️ Category: {settings.get('category', 'general').title()}\n"
        f"⏰ Last message: {hours}h {minutes}m ago\n"
        f"💤 Will revive after 2 hours"
    )

@bot.tree.command(name="revive", description="Manually trigger a question")
async def revive(interaction: discord.Interaction):
    """Manual revive"""
    settings = bot.server_settings.get(interaction.guild_id)
    
    if not settings or not settings['channel_id']:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.")
        return
    
    if interaction.channel_id != settings['channel_id']:
        await interaction.response.send_message(f"❌ This command only works in the configured channel!")
        return
    
    category = settings.get('category', DEFAULT_CATEGORY)
    questions = QUESTIONS.get(category, QUESTIONS[DEFAULT_CATEGORY])
    question = random.choice(questions)
    
    await interaction.response.send_message(f"🔄 **Manual revive!**\n*{category.title()} question:* {question}")
    
    # Reset timer
    settings['last_msg'][interaction.channel_id] = datetime.now()

@bot.tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    """Show help"""
    embed = discord.Embed(
        title="🤖 Chat Pulse",
        description="Keep your community alive with auto-revive questions!",
        color=0x00AAFF
    )
    embed.add_field(
        name="Commands",
        value=(
            "`/setup #channel` - Set revive channel\n"
            "`/category` - Choose question category\n"
            "`/status` - Check chat activity\n"
            "`/revive` - Manual question\n"
            "`/help` - Show this"
        ),
        inline=False
    )
    embed.add_field(
        name="Categories",
        value="🔫 Apex • ⛏️ Minecraft • 💣 COD • 🌍 General • 🎲 Random",
        inline=False
    )
    embed.add_field(
        name="Features",
        value="✅ Auto-revive after 2h • 50+ questions • Free forever",
        inline=False
    )
    embed.set_footer(text="Made for communities that love to chat")
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
