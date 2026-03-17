import discord
from discord import app_commands
import asyncio
import random
import os
from datetime import datetime, timedelta
import json

# Get token from environment variable
TOKEN = os.environ.get('TOKEN')

# ============= 500+ QUESTIONS =============

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
        "Who has the best voice lines? 🗣️",
        "What season did you start playing?",
        "Favorite Apex content creator?",
        "Which heirloom is the cleanest?",
        "Ranked or pubs? What's your rank?",
        "What's the most satisfying sound in Apex?",
        "If you could add one ability to any legend, what?",
        "Which legend has the best skins? 🔥",
        "What's your go-to landing spot?",
        "Triple Take or Peacekeeper?",
        "Most OP weapon ever in Apex?",
        "Which legend needs a rework?",
        "Favorite memory in Apex?",
        "What's the worst meta you've played through?",
        "If you could bring back one removed item?",
        "Which team comp is underrated?",
        "What's your hot drop strategy?",
        "How many hours do you have in Apex?",
        "Favorite battle pass skin?",
        "Which map is best? Olympus, World's Edge, or Storm Point?",
        "What's the most cracked squad you've faced?",
        "Do you play ranked or pubs more?",
        "What's your favorite limited-time mode?",
        "Which weapon needs a nerf right now?",
        "What's the most toxic thing in Apex?",
        "Favorite pro player to watch?",
        "What's your drop ship strategy?",
        "Which attachment is most important?",
        "Do you hot drop or play safe?",
        "What's your go-to character for ranked?",
        "Which legend has the best passive?",
        "Favorite finisher animation?",
        "What's the worst change they've made?",
        "Which hop-up is your favorite?",
        "Do you prefer aiming or hip fire?",
        "What's your favorite weapon combo?",
        "Which legend has the best ultimate?",
        "What's your most clutch moment?",
        "How many wins do you have?",
        "What's your favorite area to land?",
        "Do you play with friends or solo?",
        "Which legend do you hate playing against?",
        "What's your favorite Apex memory?",
        "Which season had the best battle pass?",
        "What's your favorite recolored skin?",
        "Do you buy Apex packs or battle pass only?",
        "Which legend's backstory is most interesting?",
        "What's your favorite weapon skin?",
        "Do you prefer Arenas or Battle Royale?",
        "What's the most underrated weapon?",
        "Which legend has the best tactical?",
        "What's your warmup routine?",
        "How many kills on your main?",
        "What's your favorite quote from a legend?",
        "Which map has the best loot?",
        "What's the most fun legend to play?",
        "Do you use surround sound or headphones?",
        "What's your sensitivity setting?",
        "Which legend do you want to see next?",
        "What's your favorite event so far?",
        "Do you prefer day or night maps?",
        "Which weapon skin is your grail?",
        "What's your favorite emote?",
        "Do you play other battle royales?",
        "Which legend has the best lore?",
        "What's your favorite weapon to pick up early game?",
        "Do you prefer close range or long range fights?",
        "What's your favorite place to third party?",
        "Which legend's abilities are most satisfying?",
        "What's your go-to loadout for ranked?",
        "Do you like the current meta?",
        "What's your favorite thing about Apex?",
        "What would you change about your main?",
        "Which legend has the best heirloom?",
        "What's your favorite badge?",
        "Do you track your stats?",
        "What's your highest damage game?",
        "Which legend do you want to be good at?",
        "What's the most important skill in Apex?",
        "Do you watch Apex esports?",
        "Which team do you root for?",
        "What's your favorite Apex moment in esports?",
        "Do you play with a controller or keyboard?",
        "What's your favorite setting to tweak?",
        "Which legend has the best default skin?",
        "What's your favorite weapon inspect?",
        "Do you collect badges or trackers?",
        "What's your favorite thing about your main?",
        "Which legend's abilities would you want IRL?",
        "What's your favorite map rotation?",
        "Do you prefer Ranked splits?",
        "What's the best change they've made?",
        "Which legend has the best intro quip?",
        "What's your favorite kill quip?",
        "Do you play on PC or console?",
        "What's your Apex resolution?",
        "Which legend has the best hitbox?",
        "What's your favorite weapon to run?",
        "Do you like the crafting system?",
        "What's your favorite thing to craft?",
        "Which legend has the best skydive emote?",
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
        "Diamonds - what do you craft first? 💎",
        "What's your favorite wood type?",
        "Do you sleep through night or fight?",
        "Which boss is harder: Ender Dragon or Wither?",
        "What's your favorite food in Minecraft?",
        "Do you use texture packs? Which one?",
        "What's your go-to mining level?",
        "Do you build farms or mine manually?",
        "What's your favorite animal in Minecraft?",
        "Do you play survival or creative more?",
        "What's the first structure you build?",
        "Which biome is underrated?",
        "What's your favorite update of all time?",
        "Do you play with mods? Which ones?",
        "What's your favorite enchantment?",
        "Do you use elytra or stick to ground?",
        "What's your go-to weapon enchant combo?",
        "Which villager profession is best?",
        "Do you cure zombie villagers?",
        "What's your favorite minigame on servers?",
        "Do you play on servers or single player?",
        "What's your favorite server?",
        "Do you like the Nether update?",
        "What's your favorite block?",
        "Which mob drops the best loot?",
        "Do you fish for treasure?",
        "What's your favorite music disc?",
        "Do you keep a dog as a pet in game?",
        "What's your favorite thing to automate?",
        "Do you use shaders? Which ones?",
        "What's your favorite structure to explore?",
        "Do you prefer caves or surface mining?",
        "What's your go-to height for strip mining?",
        "Do you build with function or form?",
        "What's your favorite redstone creation?",
        "Do you play hardcore mode?",
        "What's your best survival world achievement?",
        "How long have you been playing Minecraft?",
        "What's your favorite way to kill time in game?",
        "Do you like the new cave generation?",
        "What's your favorite armor trim?",
        "Do you collect every block type?",
        "What's your go-to enchantment for pickaxe?",
        "Do you use anvil or grindstone more?",
        "What's your favorite biome for a base?",
        "Do you build underground or above ground?",
        "What's your favorite tree type?",
        "Do you make item sorters?",
        "What's your favorite use for observers?",
        "Do you like the new archaeology?",
        "What's your favorite suspicious sand drop?",
        "Do you trade with piglins?",
        "What's your favorite bastion loot?",
        "Do you explore ancient cities?",
        "What's your strategy for Warden?",
        "Do you use Allays? For what?",
        "What's your favorite new mob since 1.17?",
        "Do you like the new mountains?",
        "What's your favorite cherry blossom build?",
        "Do you collect armor trims?",
        "What's your favorite trail ruin loot?",
        "Do you like the new villager trades?",
        "What's your favorite way to get XP?",
        "Do you build XP farms?",
        "What's your go-to mob farm design?",
        "Do you like the new potion effects?",
        "What's your favorite arrow type?",
        "Do you use tipped arrows?",
        "What's your favorite crossbow enchant?",
        "Do you prefer bow or crossbow?",
        "What's your favorite firework for elytra?",
        "Do you use a trident? With what enchant?",
        "What's your favorite way to travel?",
        "Do you use nether highways?",
        "What's your favorite ice boat path?",
        "Do you use leads or fences for animals?",
        "What's your favorite way to sort items?",
        "Do you name your pets?",
        "What's the best name you've given a pet?",
        "Do you make maps of your world?",
        "What's your favorite painting?",
        "Do you use armor stands for decoration?",
        "What's your favorite block for flooring?",
        "What's your favorite block for walls?",
        "Do you use different roof styles?",
        "What's your favorite lighting block?",
        "Do you use lanterns or torches?",
        "What's your favorite way to hide light sources?",
        "Do you use water in builds?",
        "What's your favorite water feature?",
        "Do you make custom trees?",
        "What's your favorite flower?",
        "Do you use bone meal for landscaping?",
        "What's your favorite pathway block?",
        "Do you build roads between bases?",
        "What's your favorite minecart use?",
        "Do you use rails for transport?",
        "What's your favorite boat type?",
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
        "Which OP weapon needs a nerf?",
        "What's your favorite COD campaign?",
        "Zombies or Multiplayer?",
        "What's the best Zombies map?",
        "Who's your favorite COD character?",
        "What's the most satisfying sound in COD?",
        "What's your favorite scorestreak?",
        "Best COD opening mission?",
        "What's the most toxic COD lobby moment?",
        "Which COD had the best movement?",
        "What's your favorite weapon skin?",
        "Do you play Warzone? Loadout preference?",
        "What's your favorite Gulag strategy?",
        "Best landing spot in Warzone?",
        "What's the most OP Warzone weapon ever?",
        "Do you buy loadout or wait for free?",
        "What's your favorite perk?",
        "Which perk is useless?",
        "What's your favorite lethal equipment?",
        "What's your favorite tactical?",
        "Best wildcard in create-a-class?",
        "What's your go-to attachment setup?",
        "Do you use laser sights?",
        "What's your favorite optic?",
        "Do you use suppressors?",
        "What's your favorite ammunition type?",
        "Do you play Hardcore mode?",
        "What's your favorite party mode?",
        "Best COD for SnD?",
        "What's your SnD strategy?",
        "Do you play competitive?",
        "What's your favorite CDL team?",
        "Who's your favorite pro player?",
        "What's the best COD moment in esports?",
        "Do you watch COD events?",
        "What's your favorite clutch memory?",
        "What's the best ninja defuse you've seen?",
        "Do you play with friends or solo?",
        "What's your best killstreak ever?",
        "What's the most kills you've gotten in a game?",
        "Do you go for nukes?",
        "What's your favorite nuke calling card?",
        "Best COD for quick scoping?",
        "Do you snipe? Favorite sniper?",
        "What's your favorite quickscope map?",
        "Do you use shotguns?",
        "What's your favorite shotgun?",
        "Do you use melee weapons?",
        "What's your favorite melee?",
        "What's your favorite pistol?",
        "Do you use launchers?",
        "What's your favorite kill confirmed map?",
        "Best map for Domination?",
        "What's your favorite Hardpoint hill?",
        "Do you play Control?",
        "What's your favorite mode in ranked?",
        "Do you play 6v6 or 10v10?",
        "What's your favorite Ground War map?",
        "Do you play Invasion?",
        "What's your favorite vehicle in Ground War?",
        "Do you like the new movement mechanics?",
        "What's your favorite COD YouTuber?",
        "Who's the funniest COD streamer?",
        "What's your favorite COD video?",
        "Do you watch tips and tricks videos?",
        "What's the best tip for new players?",
        "What's your sensitivity setting?",
        "Do you use aim assist?",
        "What's your button layout?",
        "Do you play claw or regular?",
        "What's your controller setup?",
        "Do you use paddles?",
        "What's your FOV setting?",
        "Do you use a monitor or TV?",
        "What's your audio setup?",
        "Do you use headphones or speakers?",
        "What's the best sound setting?",
        "Do you use a gaming chair?",
        "What's your favorite COD soundtrack?",
        "Best menu music in COD?",
        "What's your favorite COD intro?",
        "Do you buy battle passes?",
        "What's the best battle pass skin?",
        "Do you buy store bundles?",
        "What's the best bundle you've bought?",
        "Do you grind camos?",
        "What's the hardest camo grind?",
        "What's your favorite mastery camo?",
        "Do you have Damascus/Dark Matter?",
        "What's your favorite calling card?",
        "Do you do operator missions?",
        "Who's your favorite operator?",
        "What's your favorite operator skin?",
        "Do you use finishers?",
        "What's your favorite finisher?",
        "Do you play private matches?",
        "What's your favorite custom game mode?",
        "Do you play against bots?",
        "What's your favorite way to warm up?",
        "How long have you been playing COD?",
        "What was your first COD game?",
        "Which COD did you play the most?",
        "What's your favorite COD memory?",
        "Who did you play with back in the day?",
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
        "What's the best advice you've ever received?",
        "What's the most beautiful place you've visited?",
        "If you could time travel, past or future?",
        "What's your biggest fear?",
        "What's something you're proud of?",
        "Who inspires you the most?",
        "What's your favorite smell?",
        "What's the most adventurous thing you've done?",
        "If you could meet anyone dead or alive, who?",
        "What's your guilty pleasure?",
        "What's the best gift you've ever received?",
        "What's a skill you want to learn?",
        "What's your favorite season and why?",
        "Do you prefer sunrise or sunset?",
        "What's your favorite type of weather?",
        "What's the best decision you've made?",
        "What's something you'd tell your younger self?",
        "What's your favorite family tradition?",
        "Do you believe in luck?",
        "What's your favorite holiday?",
        "What's the best compliment you've received?",
        "What's something that always makes you laugh?",
        "What's your favorite joke?",
        "What's the most random fact you know?",
        "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
        "What's the first thing you'd buy after winning the lottery? 💰",
        "What's your go-to karaoke song? 🎤",
        "Most embarrassing memory from school?",
        "If you were a YouTuber, what content? 📹",
        "What's a smell that brings back memories?",
        "Would you want to know the date of your death?",
        "If you could delete one thing from the internet, what? 🌐",
        "What's your favorite app on your phone?",
        "Do you prefer Android or iPhone?",
        "What's your favorite video game of all time?",
        "Do you play mobile games? Which ones?",
        "What's your favorite board game?",
        "Do you prefer cards or video games?",
        "What's your favorite sport to watch?",
        "Do you play any sports?",
        "What's your favorite workout?",
        "Do you prefer gym or outdoor exercise?",
        "What's your favorite healthy food?",
        "What's your favorite junk food?",
        "Do you cook? What's your specialty?",
        "What's your favorite restaurant?",
        "Do you prefer sweet or savory?",
        "What's your favorite dessert?",
        "What's your favorite drink?",
        "Do you prefer coffee or tea?",
        "What's your favorite breakfast?",
        "What's your go-to midnight snack?",
        "Do you like spicy food? How spicy?",
        "What's a food you hated as a kid but love now?",
        "What's a food you loved as a kid but hate now?",
        "What's your favorite cuisine?",
        "Do you prefer cooking at home or eating out?",
        "What's your favorite fast food?",
        "Do you have any food allergies?",
        "What's your favorite fruit?",
        "What's your favorite vegetable?",
        "Do you have a sweet tooth?",
        "What's your favorite ice cream flavor?",
        "Do you like pineapple on pizza?",
        "What's your go-to pizza topping?",
        "What's your favorite sandwich?",
        "Do you prefer burgers or hot dogs?",
        "What's your favorite soda?",
        "Do you drink energy drinks? Which ones?",
        "What's your favorite alcoholic drink?",
        "Do you prefer beer or cocktails?",
        "What's your favorite movie genre?",
        "Who's your favorite actor?",
        "Who's your favorite actress?",
        "What's the last movie you watched?",
        "Do you prefer movies or TV shows?",
        "What's your favorite TV show of all time?",
        "What are you currently watching?",
        "Do you binge watch or watch weekly?",
        "What's your favorite streaming service?",
        "Do you prefer Netflix, Hulu, or Disney+?",
        "What's your favorite documentary?",
        "Do you watch anime? Which one?",
        "What's your favorite animated movie?",
        "Who's your favorite Disney character?",
        "What's your favorite book?",
        "Who's your favorite author?",
        "Do you prefer physical books or ebooks?",
        "What's the last book you read?",
        "Do you listen to audiobooks?",
        "What's your favorite music genre?",
        "Who's your favorite artist/band?",
        "What's the last concert you attended?",
        "Do you play any instruments?",
        "What's your favorite decade for music?",
        "Do you prefer headphones or speakers?",
        "What's your favorite podcast?",
        "Do you listen to music while working?",
        "What's your favorite workout song?",
        "What's your favorite driving song?",
        "What's your go-to shower song?",
        "Do you sing in the car?",
        "What's your favorite childhood TV show?",
        "What's your favorite childhood movie?",
        "What was your favorite toy growing up?",
        "What's your favorite memory from school?",
        "Who was your favorite teacher?",
        "What subject did you excel in?",
        "What subject did you struggle with?",
        "Did you go to college? What for?",
        "What's your dream job?",
        "What was your first job?",
        "What's the worst job you've had?",
        "What's your current job?",
        "Do you like your job?",
        "What's your dream career?",
        "If money wasn't an issue, what would you do?",
        "What's your biggest goal right now?",
        "What's something you want to achieve this year?",
        "Where do you see yourself in 5 years?",
        "What's your biggest regret?",
        "What's something you'd do differently?",
        "What's the best life advice you have?",
        "What's your philosophy on life?",
        "What makes you happy?",
        "What's your happy place?",
        "What do you do to relax?",
        "How do you deal with stress?",
        "What's your self-care routine?",
        "Do you meditate?",
        "Do you exercise regularly?",
        "How many hours of sleep do you need?",
        "Are you a morning person or night owl?",
        "What's your morning routine?",
        "What's your nighttime routine?",
        "Do you make your bed every day?",
        "What's a habit you want to break?",
        "What's a habit you want to start?",
        "What's something you do every day?",
        "What's your favorite day of the week?",
        "What's your least favorite day?",
        "Do you prefer weekends or weekdays?",
        "What's your favorite time of day?",
        "Do you watch the sunrise?",
        "Do you watch the sunset?",
        "What's your favorite thing about nature?",
        "Do you prefer beach or mountains?",
        "What's your favorite animal?",
        "Do you have any pets?",
        "What's your pet's name?",
        "Do you prefer dogs or cats?",
        "What's the best pet you've had?",
        "Would you rather live in the city or countryside?",
        "What's your dream home like?",
        "Do you prefer hot or cold weather?",
        "What's your favorite thing to do on a rainy day?",
        "What's your favorite thing to do on a sunny day?",
        "Do you prefer summer or winter?",
        "What's your favorite holiday tradition?",
        "How do you celebrate your birthday?",
        "What's the best birthday you've had?",
        "Do you prefer parties or intimate gatherings?",
        "Are you introverted or extroverted?",
        "Do you prefer small groups or large crowds?",
        "What's your social battery like?",
        "Do you enjoy meeting new people?",
        "How do you make friends?",
        "What do you value most in a friend?",
        "What's the best quality in a person?",
        "What's a red flag in people?",
        "What's something you can't stand?",
        "What's your pet peeve?",
        "What makes you angry?",
        "What makes you sad?",
        "What makes you excited?",
        "What's your love language?",
        "How do you show you care?",
        "How do you like to be comforted?",
        "What's your favorite way to spend a day off?",
        "What do you do when you're bored?",
        "What's your favorite hobby?",
        "Do you have any collections?",
        "What's something you're passionate about?",
        "What could you talk about for hours?",
        "What's something new you want to try?",
        "What's your biggest adventure so far?",
        "What's on your bucket list?",
        "Where do you want to travel?",
        "What's your dream vacation?",
        "Have you ever been out of the country?",
        "What's the best trip you've taken?",
        "What's the worst trip you've taken?",
        "Do you prefer road trips or flights?",
        "What's your favorite mode of transportation?",
        "Do you like camping?",
        "Have you ever been camping?",
        "What's your favorite outdoor activity?",
        "Do you like hiking?",
        "What's the best hike you've done?",
        "Do you prefer solo travel or group?",
        "What's your favorite memory with friends?",
        "What's your favorite memory with family?",
        "What's something you're grateful for?",
        "What's something that made you smile today?",
        "What's the last thing that made you laugh?",
        "What's the last thing that made you cry?",
        "What's the most beautiful thing you've seen?",
        "What's the most peaceful place you've been?",
        "What's the most exciting thing you've done?",
        "What's the most terrifying thing you've done?",
        "What's something that surprised you?",
        "What's something that changed your life?",
        "What's a lesson you learned the hard way?",
        "What's something you wish you knew earlier?",
        "What's your biggest strength?",
        "What's your biggest weakness?",
        "What's something you're working on improving?",
        "What's something you like about yourself?",
        "What's something you'd like to change?",
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
        "If you could delete one thing from the internet, what? 🌐",
        "What's the weirdest dream you've ever had?",
        "If you could talk to animals, which one first?",
        "What's the most useless invention?",
        "If you were a ghost, where would you haunt?",
        "What's the best prank you've pulled?",
        "What's the worst prank pulled on you?",
        "If you could be any age for a week, what age?",
        "What's something that shouldn't be scary but is?",
        "What's the most random thing in your room right now?",
        "If you had to eat one color of food for a year, what color?",
        "What's the worst texture?",
        "What's the best sound in the world?",
        "What's the worst sound?",
        "If you were a kitchen appliance, what would you be?",
        "What's the most overrated thing?",
        "What's the most underrated thing?",
        "If you could instantly learn any language, which?",
        "What's a word you always mispronounce?",
        "What's a word you can never spell right?",
        "What's your favorite tongue twister?",
        "Do you have any recurring dreams?",
        "What's the weirdest thing you've eaten?",
        "What's something you believed as a kid that's ridiculous?",
        "If you were a superhero, what would your power be?",
        "What would your superhero name be?",
        "What's your villain origin story?",
        "If you could be any fictional creature, what?",
        "What's your spirit animal?",
        "What would be your walk-up song?",
        "If you were a wrestler, what would your entrance music be?",
        "What's the most random subreddit you follow?",
        "What's the best Wikipedia rabbit hole you've been down?",
        "What's the most interesting Wikipedia page?",
        "If you could ask a time traveler one question, what?",
        "What would you bring to a deserted island?",
        "What's the first thing you'd do in a zombie apocalypse?",
        "What's your survival strategy?",
        "Would you rather live in a treehouse or an underground bunker?",
        "What's your dream treehouse like?",
        "What's your dream bunker like?",
        "If you could live in any video game world, which?",
        "What's your favorite in-game item?",
        "What game has the best soundtrack?",
        "If you could be any video game character, who?",
        "What's the most satisfying game mechanic?",
        "What's the most annoying game mechanic?",
        "Do you prefer single-player or multiplayer?",
        "What's your favorite indie game?",
        "What's the most overhyped game?",
        "What's the most underrated game?",
        "What game has the best story?",
        "What game has the best graphics?",
        "What's the hardest game you've beaten?",
        "What game did you give up on?",
        "What's your favorite game franchise?",
        "What's a game you can play over and over?",
        "What's your go-to game when bored?",
        "Do you prefer console, PC, or mobile?",
        "What's your favorite console of all time?",
        "Do you collect any gaming memorabilia?",
        "What's your favorite gaming memory?",
        "Who's your favorite gaming YouTuber?",
        "What's your favorite gaming streamer?",
        "Do you watch esports? Which games?",
        "Have you been to any gaming events?",
        "What's your favorite gaming snack?",
        "Do you have a gaming setup? What's in it?",
        "What's your favorite RGB color?",
        "Do you prefer mechanical or membrane keyboard?",
        "What's your mouse DPI?",
        "Do you use controller for PC games?",
        "What's your favorite controller?",
        "Do you prefer wireless or wired?",
        "What's your headset?",
        "Do you use surround sound?",
        "What's your monitor size?",
        "What's your refresh rate?",
        "Do you play in the dark or with lights on?",
        "What's your gaming posture?",
        "Do you game in bed?",
        "What's your favorite game to play with friends?",
        "What's your favorite game to play alone?",
        "What's a game you're embarrassed to admit you like?",
        "What's a game everyone should play at least once?",
        "What's the best opening level in a game?",
        "What's the best final boss?",
        "What's the most emotional game moment?",
        "What game made you cry?",
        "What game made you rage quit?",
        "What's the best plot twist in gaming?",
        "What's your favorite easter egg?",
        "What's the best hidden secret in a game?",
        "What game has the best post-game content?",
        "What's your favorite DLC?",
        "What's the worst DLC?",
        "Do you pre-order games?",
        "Do you buy games at launch or wait for sales?",
        "What's the best game deal you've gotten?",
        "What's the most you've spent on a game?",
        "Do you buy physical or digital?",
        "What's your favorite game art style?",
        "Do you prefer realistic or stylized graphics?",
        "What's the most beautiful game world?",
        "What game has the best atmosphere?",
        "What game has the best music?",
        "Who's your favorite video game composer?",
        "What's your favorite video game track?",
        "What game has the best sound design?",
        "What's your favorite voice acting in a game?",
        "Who's your favorite video game voice actor?",
        "What's the funniest game you've played?",
        "What's the scariest game you've played?",
        "What's the most relaxing game?",
        "What's the most stressful game?",
        "What game has the best multiplayer?",
        "What game has the best community?",
        "What game has the worst community?",
        "What's your favorite gaming genre?",
        "What genre do you avoid?",
        "What's a genre you want to get into?",
        "What's your most anticipated upcoming game?",
        "What game announcement would make you lose your mind?",
        "If you could make one game exist, what would it be?",
        "What's your favorite game theory?",
        "Who's the most overrated video game character?",
        "Who's the most underrated?",
        "What's the best video game quote?",
        "What's the worst?",
        "What game has the best tutorial?",
        "What game has the worst?",
        "What's the most innovative game mechanic?",
        "What's the most overused mechanic?",
        "Do you like crafting in games?",
        "Do you like survival games?",
        "Do you like battle royale games?",
        "Do you like open world games?",
        "What's your favorite open world?",
        "Do you like linear or open world more?",
        "Do you complete side quests or main story?",
        "Are you a completionist?",
        "Do you go for 100% achievements?",
        "What's the hardest achievement you've earned?",
        "What achievement are you most proud of?",
        "Do you use mods? Favorite mod?",
        "What's a game that's better with mods?",
        "What's a game that shouldn't be modded?",
        "Do you play vanilla or modded?",
        "What's your favorite vanilla game?",
        "What's your favorite modded experience?",
    ]
}

# ============= BOT SETUP =============

class CategorySelect(discord.ui.Select):
    def __init__(self, bot):
        options = [
            discord.SelectOption(label="Apex Legends", value="apex", emoji="🔫", description="100+ Apex questions"),
            discord.SelectOption(label="Minecraft", value="minecraft", emoji="⛏️", description="100+ Minecraft questions"),
            discord.SelectOption(label="Call of Duty", value="cod", emoji="💣", description="100+ COD questions"),
            discord.SelectOption(label="General Life", value="general", emoji="🌍", description="100+ life questions"),
            discord.SelectOption(label="Random Fun", value="random", emoji="🎲", description="100+ random questions"),
        ]
        super().__init__(placeholder="🎯 Choose your category...", min_values=1, max_values=1, options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        category = self.values[0]
        
        if guild_id not in self.bot.server_settings:
            await interaction.response.send_message("❌ Please run `/setup` first!", ephemeral=True)
            return
        
        self.bot.server_settings[guild_id]['category'] = category
        
        embed = discord.Embed(
            title="✅ Category Updated!",
            description=f"Now using **{category.title()}** category with **{len(QUESTIONS[category])}** questions!",
            color=0x00FF00
        )
        embed.set_footer(text=f"Example: {random.choice(QUESTIONS[category])}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class CategoryView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.add_item(CategorySelect(bot))

class ChatPulseBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.check_interval = 60
        self.server_settings = {}  # guild_id: {'channel_id': int, 'category': str, 'last_msg': dict, 'cooldown': int}
        self.settings_lock = asyncio.Lock()

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Slash commands synced")

    async def on_ready(self):
        print(f'✅ Chat Pulse has connected to Discord!')
        print(f'📊 Bot is in {len(self.guilds)} server(s)')
        print(f'💬 Loaded {sum(len(q) for q in QUESTIONS.values())} questions across {len(QUESTIONS)} categories!')
        
        # Initialize settings for each guild
        for guild in self.guilds:
            if str(guild.id) not in self.server_settings:
                self.server_settings[str(guild.id)] = {
                    'channel_id': None,
                    'category': 'general',
                    'last_msg': {},
                    'cooldown': 2,
                    'custom_questions': []
                }
        
        # Start the inactivity checker
        self.bg_task = self.loop.create_task(self.check_inactivity())
        print(f'⏰ Inactivity checker started (checking every {self.check_interval}s)')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Track messages in monitored channels
        if message.guild:
            guild_id = str(message.guild.id)
            if guild_id in self.server_settings:
                settings = self.server_settings[guild_id]
                if settings['channel_id'] == message.channel.id:
                    settings['last_msg'][str(message.channel.id)] = datetime.now().isoformat()

    async def check_inactivity(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                for guild_id, settings in self.server_settings.items():
                    if settings['channel_id']:
                        channel = self.get_channel(settings['channel_id'])
                        if channel:
                            channel_id_str = str(channel.id)
                            
                            # Initialize if needed
                            if channel_id_str not in settings['last_msg']:
                                settings['last_msg'][channel_id_str] = datetime.now().isoformat()
                            
                            # Check inactivity
                            last_time = datetime.fromisoformat(settings['last_msg'][channel_id_str])
                            time_since = datetime.now() - last_time
                            
                            if time_since >= timedelta(hours=settings['cooldown']):
                                # Get question from selected category
                                category = settings.get('category', 'general')
                                questions = QUESTIONS.get(category, QUESTIONS['general'])
                                
                                # Include custom questions if any
                                all_questions = questions + settings.get('custom_questions', [])
                                question = random.choice(all_questions)
                                
                                embed = discord.Embed(
                                    title=f"🌱 Chat's been quiet for {settings['cooldown']} hours!",
                                    description=f"**{category.title()} Question:**\n{question}",
                                    color=0x00AAFF
                                )
                                embed.set_footer(text="Chat Pulse • Keeping communities alive")
                                
                                await channel.send(embed=embed)
                                print(f"📤 Sent {category} revive in guild {guild_id}")
                                
                                # Reset timer
                                settings['last_msg'][channel_id_str] = datetime.now().isoformat()
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ Error in check_inactivity: {e}")
                await asyncio.sleep(self.check_interval)

bot = ChatPulseBot()

# ============= SLASH COMMANDS =============

@bot.tree.command(name="setup", description="Set the channel for Chat Pulse to revive")
@app_commands.describe(channel="The channel to watch and revive")
async def setup(interaction: discord.Interaction, channel: discord.TextChannel):
 await interaction.response.defer()
    """Set up the revive channel"""
    guild_id = str(interaction.guild_id)
    
    async with bot.settings_lock:
        if guild_id not in bot.server_settings:
            bot.server_settings[guild_id] = {
                'channel_id': None,
                'category': 'general',
                'last_msg': {},
                'cooldown': 2,
                'custom_questions': []
            }
        bot.server_settings[guild_id]['channel_id'] = channel.id
        bot.server_settings[guild_id]['last_msg'][str(channel.id)] = datetime.now().isoformat()
    
    embed = discord.Embed(
        title="✅ Chat Pulse Setup Complete!",
        description=f"📌 **Channel:** {channel.mention}\n"
                   f"🗂️ **Category:** {bot.server_settings[guild_id]['category'].title()}\n"
                   f"⏰ **Cooldown:** {bot.server_settings[guild_id]['cooldown']} hours\n"
                   f"💡 Use `/category` to change categories!",
        color=0x00FF00
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="category", description="Open category selection menu")
async def category(interaction: discord.Interaction):
    """Choose question category"""
    guild_id = str(interaction.guild_id)
    
    if guild_id not in bot.server_settings or not bot.server_settings[guild_id]['channel_id']:
        await interaction.response.send_message("❌ Please run `/setup` first!", ephemeral=True)
        return
    
    view = CategoryView(bot)
    await interaction.response.send_message("📋 **Select a category:**", view=view, ephemeral=True)

@bot.tree.command(name="revive", description="Manually trigger a revive question")
async def revive(interaction: discord.Interaction):
    """Manual revive"""
    guild_id = str(interaction.guild_id)
    settings = bot.server_settings.get(guild_id)
    
    if not settings or not settings['channel_id']:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.", ephemeral=True)
        return
    
    category = settings.get('category', 'general')
    questions = QUESTIONS.get(category, QUESTIONS['general'])
    all_questions = questions + settings.get('custom_questions', [])
    question = random.choice(all_questions)
    
    embed = discord.Embed(
        title="🔄 Manual Revive!",
        description=f"**{category.title()} Question:**\n{question}",
        color=0x00AAFF
    )
    await interaction.response.send_message(embed=embed)
    
    # Reset timer
    if str(interaction.channel_id) in settings['last_msg']:
        settings['last_msg'][str(interaction.channel_id)] = datetime.now().isoformat()

@bot.tree.command(name="status", description="Check chat activity status")
async def status(interaction: discord.Interaction):
    """Check current status"""
    guild_id = str(interaction.guild_id)
    settings = bot.server_settings.get(guild_id)
    
    if not settings or not settings['channel_id']:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.", ephemeral=True)
        return
    
    channel = bot.get_channel(settings['channel_id'])
    if not channel:
        await interaction.response.send_message("❌ Configured channel not found!", ephemeral=True)
        return
    
    channel_id_str = str(channel.id)
    if channel_id_str not in settings['last_msg']:
        settings['last_msg'][channel_id_str] = datetime.now().isoformat()
    
    last_time = datetime.fromisoformat(settings['last_msg'][channel_id_str])
    time_since = datetime.now() - last_time
    hours = int(time_since.total_seconds() / 3600)
    minutes = int((time_since.total_seconds() / 60) % 60)
    
    embed = discord.Embed(
        title="📊 Chat Pulse Status",
        color=0x00AAFF
    )
    embed.add_field(name="📌 Channel", value=channel.mention, inline=True)
    embed.add_field(name="🗂️ Category", value=settings['category'].title(), inline=True)
    embed.add_field(name="⏰ Cooldown", value=f"{settings['cooldown']} hours", inline=True)
    embed.add_field(name="💬 Last Message", value=f"{hours}h {minutes}m ago", inline=True)
    embed.add_field(name="📚 Questions", value=f"{len(QUESTIONS[settings['category']])}+", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="cooldown", description="Set hours before auto-revive (1-6 hours)")
@app_commands.describe(hours="Number of hours (1-6)")
async def cooldown(interaction: discord.Interaction, hours: int):
    """Change revive cooldown"""
    guild_id = str(interaction.guild_id)
    settings = bot.server_settings.get(guild_id)
    
    if not settings or not settings['channel_id']:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.", ephemeral=True)
        return
    
    if hours < 1 or hours > 6:
        await interaction.response.send_message("❌ Hours must be between 1 and 6!", ephemeral=True)
        return
    
    settings['cooldown'] = hours
    
    await interaction.response.send_message(f"✅ Cooldown set to **{hours} hours**!")

@bot.tree.command(name="remove", description="Remove Chat Pulse setup from this server")
async def remove(interaction: discord.Interaction):
    """Remove bot setup"""
    guild_id = str(interaction.guild_id)
    
    if guild_id not in bot.server_settings:
        await interaction.response.send_message("❌ No setup found for this server!", ephemeral=True)
        return
    
    # Create confirmation buttons
    view = discord.ui.View()
    confirm = discord.ui.Button(label="✅ Yes, remove", style=discord.ButtonStyle.danger)
    cancel = discord.ui.Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        bot.server_settings[guild_id] = {
            'channel_id': None,
            'category': 'general',
            'last_msg': {},
            'cooldown': 2,
            'custom_questions': []
        }
        await interaction.response.send_message("✅ Chat Pulse setup removed! Use `/setup` to start again.")
    
    async def cancel_callback(interaction):
        await interaction.response.send_message("❌ Removal cancelled.", ephemeral=True)
    
    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    
    view.add_item(confirm)
    view.add_item(cancel)
    
    await interaction.response.send_message("⚠️ **Are you sure you want to remove Chat Pulse?**", view=view)

@bot.tree.command(name="addquestion", description="Add a custom question to your server")
@app_commands.describe(question="Your custom question")
async def add_question(interaction: discord.Interaction, question: str):
    """Add custom question"""
    guild_id = str(interaction.guild_id)
    settings = bot.server_settings.get(guild_id)
    
    if not settings:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.", ephemeral=True)
        return
    
    if 'custom_questions' not in settings:
        settings['custom_questions'] = []
    
    settings['custom_questions'].append(question)
    
    await interaction.response.send_message(f"✅ Question added! Now have {len(settings['custom_questions'])} custom questions.")

@bot.tree.command(name="settings", description="View all current settings")
async def show_settings(interaction: discord.Interaction):
    """Show all settings"""
    guild_id = str(interaction.guild_id)
    settings = bot.server_settings.get(guild_id)
    
    if not settings or not settings['channel_id']:
        await interaction.response.send_message("❌ Bot not set up yet! Use `/setup` first.", ephemeral=True)
        return
    
    channel = bot.get_channel(settings['channel_id'])
    channel_name = channel.mention if channel else "Unknown"
    
    embed = discord.Embed(
        title="⚙️ Chat Pulse Settings",
        color=0x00AAFF
    )
    embed.add_field(name="📌 Channel", value=channel_name, inline=True)
    embed.add_field(name="🗂️ Category", value=settings['category'].title(), inline=True)
    embed.add_field(name="⏰ Cooldown", value=f"{settings['cooldown']} hours", inline=True)
    embed.add_field(name="📚 Category Questions", value=str(len(QUESTIONS[settings['category']])), inline=True)
    embed.add_field(name="✨ Custom Questions", value=str(len(settings.get('custom_questions', []))), inline=True)
    embed.add_field(name="📊 Total Questions", value=str(len(QUESTIONS[settings['category']]) + len(settings.get('custom_questions', []))), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Check if bot is alive")
async def ping(interaction: discord.Interaction):
    """Pong!"""
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 **Pong!** Latency: `{latency}ms`")

@bot.tree.command(name="stats", description="Show bot statistics")
async def stats(interaction: discord.Interaction):
    """Bot stats"""
    total_servers = len(bot.guilds)
    total_questions = sum(len(q) for q in QUESTIONS.values())
    total_categories = len(QUESTIONS)
    
    embed = discord.Embed(
        title="📊 Chat Pulse Statistics",
        color=0x00AAFF
    )
    embed.add_field(name="🖥️ Servers", value=str(total_servers), inline=True)
    embed.add_field(name="📚 Questions", value=str(total_questions), inline=True)
    embed.add_field(name="🗂️ Categories", value=str(total_categories), inline=True)
    embed.add_field(name="⏰ Uptime", value="24/7", inline=True)
    embed.add_field(name="💎 Version", value="Ultimate 1.0", inline=True)
    embed.add_field(name="👑 Creator", value="You!", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="vote", description="Vote for Chat Pulse")
async def vote(interaction: discord.Interaction):
    """Vote link"""
    embed = discord.Embed(
        title="🗳️ Vote for Chat Pulse!",
        description="Support the bot by voting!\n\n[🔗 Vote on top.gg](https://top.gg)",
        color=0x00AAFF
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="donate", description="Support Chat Pulse development")
async def donate(interaction: discord.Interaction):
    """Donation link"""
    embed = discord.Embed(
        title="☕ Support Chat Pulse",
        description="Love the bot? Consider supporting!\n\n[💰 Buy Me a Coffee](https://buymeacoffee.com/omar_fattah)\n[❤️ Become a Patron](https://www.patreon.com/cw/Omar_fattah)",
        color=0x00AAFF
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="feedback", description="Send feedback to the developer")
@app_commands.describe(message="Your feedback or suggestion")
async def feedback(interaction: discord.Interaction, message: str):
    """Send feedback"""
    # Log feedback to console (you could add a database/webhook later)
    print(f"📝 FEEDBACK from {interaction.user} in {interaction.guild}: {message}")
    await interaction.response.send_message("✅ Thank you for your feedback! The developer has received it.", ephemeral=True)

@bot.tree.command(name="help", description="Show all Chat Pulse commands")
async def help_command(interaction: discord.Interaction):
    """Show help"""
    embed = discord.Embed(
        title="🤖 Chat Pulse - Ultimate Revival Bot",
        description="Keep your community alive with auto-revive questions!",
        color=0x00AAFF
    )
    
    embed.add_field(
        name="📝 **Setup Commands**",
        value=(
            "`/setup #channel` - Set revive channel\n"
            "`/category` - Choose question category\n"
            "`/cooldown [1-6]` - Change revive time\n"
            "`/remove` - Delete setup\n"
            "`/settings` - View current config"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 **Interaction Commands**",
        value=(
            "`/revive` - Manual question\n"
            "`/status` - Check activity\n"
            "`/addquestion [text]` - Add custom question\n"
            "`/ping` - Check bot health"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 **Info Commands**",
        value=(
            "`/stats` - Bot statistics\n"
            "`/vote` - Vote for the bot\n"
            "`/donate` - Support development\n"
            "`/feedback` - Send suggestions\n"
            "`/help` - Show this menu"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🗂️ **Categories & Questions**",
        value=(
            f"🔫 **Apex:** {len(QUESTIONS['apex'])} questions\n"
            f"⛏️ **Minecraft:** {len(QUESTIONS['minecraft'])} questions\n"
            f"💣 **COD:** {len(QUESTIONS['cod'])} questions\n"
            f"🌍 **General:** {len(QUESTIONS['general'])} questions\n"
            f"🎲 **Random:** {len(QUESTIONS['random'])} questions\n"
            f"✨ **Total:** {sum(len(q) for q in QUESTIONS.values())}+ questions!"
        ),
        inline=False
    )
    
    embed.set_footer(text="Chat Pulse • Keeping communities alive • 100% Free Forever")
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
