import discord
from discord import app_commands
import asyncio
import random
import os
import sqlite3
import json
from datetime import datetime, timedelta
import aiosqlite
from typing import Optional, List, Dict, Any
import traceback

# ==================== CONFIG ====================
TOKEN = os.environ.get('TOKEN')
DB_PATH = 'chatpulse.db'

# ==================== DEFAULT QUESTIONS (700+) ====================
DEFAULT_QUESTIONS = {
    "apex": [
        "Who's your main in Apex and why? 🔫",
        "Hot take: Which legend is actually overrated?",
        "What's the dumbest way you've died in Apex? 💀",
        "Kraber or Mastiff? GO!",
        "Which POI is your drop spot and why?",
        "Controller or MnK? (let the debate begin...)",
        "Favorite weapon loadout right now?",
        "Which legend has the best voice lines? 🗣️",
        "What's the most satisfying sound in Apex? (that shield break though 👌)",
        "If you could bring back one removed feature/weapon, what would it be?",
        "Who's your least favorite legend to play against?",
        "What's your go-to landing spot for hot drops?",
        "Which heirloom is the cleanest?",
        "Thoughts on the current ranked system?",
        "What's a tip that would help new players?",
        "Which legend needs a rework the most?",
        "What's your record kill/damage game? 📊",
        "Which season did you start playing?",
        "Favorite Apex content creator to watch?",
        "If you could buff one weapon right now, which one?",
        "What's the most cracked squad you've ever faced?",
        "Which legend has the best skins? 🔥",
        "What's your favorite map?",
        "Do you prefer ranked or pubs?",
        "What's your go-to character for ranked?",
        "Which weapon needs a nerf?",
        "What's the most underrated legend?",
        "Who has the best heirloom?",
        "What's your favorite finisher?",
        "Which legend has the best passive ability?",
        "What's the best hop-up in the game?",
        "Do you hot drop or play safe?",
        "What's your favorite weapon combo?",
        "Which attachment is most important?",
        "What's your sensitivity settings?",
        "Do you play on PC or console?",
        "What's your favorite memory in Apex?",
        "Who's your favorite pro player?",
        "What's the best team comp right now?",
        "Which legend has the best ultimate?",
        "What's your favorite area to land?",
        "Do you play with friends or solo?",
        "What's the worst meta you've played through?",
        "Which legend do you want to see next?",
        "What's your favorite event so far?",
        "Do you buy the battle pass?",
        "What's your favorite skin in the game?",
        "Which legend has the best lore?",
        "What's your favorite weapon to pick up early game?",
        "Do you prefer close range or long range fights?",
        "What's your favorite place to third party?",
        "Which legend's abilities are most satisfying?",
        "What's your go-to loadout for ranked?",
        "Do you like the current meta?",
        "What would you change about your main?",
        "Do you track your stats?",
        "What's your highest damage game?",
        "Which legend do you want to be good at?",
        "What's the most important skill in Apex?",
        "Do you watch Apex esports?",
        "Which team do you root for?",
        "What's your favorite Apex moment in esports?",
        "What's your favorite setting to tweak?",
        "Do you collect badges?",
        "What's your favorite badge?",
        "Which legend has the best default skin?",
        "What's your favorite weapon inspect?",
        "Do you use the firing range to warm up?",
        "What's your warmup routine?",
        "How many hours do you have in Apex?",
        "What's your favorite thing about Apex?",
        "What's the most annoying legend to play against?",
        "Which legend has the best tactical ability?",
        "What's your favorite quote from a legend?",
        "Do you play other battle royales?",
        "Which map has the best loot?",
        "What's your favorite weapon skin?",
        "Do you prefer Arenas or Battle Royale?",
        "What's your favorite limited-time mode?",
        "Which hop-up is your favorite?",
        "What's the most toxic thing in Apex?",
        "Do you prefer day or night maps?",
        "What's your favorite weapon to run?",
        "Do you like the crafting system?",
        "What's your favorite thing to craft?",
        "Which legend has the best skydive emote?",
        "What's your favorite intro quip?",
        "What's your favorite kill quip?",
        "Do you play with a controller or keyboard?",
        "What's your FOV setting?",
        "Do you use surround sound?",
        "What's your favorite legend to play with friends?",
        "Which legend do you main in ranked?",
        "What's your favorite weapon to use in Arenas?",
        "Do you like the new map changes?",
        "What's your favorite POI in the new map?",
        "Which legend has the best hitbox?",
        "What's your favorite way to rotate?",
        "Do you use jump towers or balloons?",
        "What's your favorite care package weapon?",
        "Do you prefer light, heavy, or energy ammo?",
        "What's your favorite sight?",
        "Do you use the new legend?",
        "What's your opinion on the current battle pass?",
        "Do you complete daily challenges?",
        "What's your favorite weekly challenge?",
        "Do you play during events?",
        "What's your favorite event reward?",
        "Which legend has the best trackers?",
        "What's your favorite stat to track?",
        "Do you have 20 kill badge? 4k damage?",
        "What's your goal in Apex?",
        "How did you start playing Apex?",
        "What keeps you playing Apex?"
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
        "Do you like the new boats with chests?",
        "What's your favorite animal to breed?",
        "Do you have a favorite seed?",
        "What's the best seed you've found?",
        "Do you use coordinates or explore naturally?",
        "What's your favorite Y-level to mine?",
        "Do you use beacons? For what?",
        "What's your favorite potion effect?",
        "Do you use shields?",
        "What's your favorite sword enchant?",
        "Do you use axes as weapons?",
        "What's your favorite armor set?",
        "Do you use netherite or diamond?",
        "What's your favorite trim combination?",
        "Do you collect every music disc?",
        "What's your favorite disc to play?",
        "Do you use jukeboxes in builds?",
        "What's your favorite redstone component?",
        "Do you understand comparators?",
        "What's your favorite thing to do with pistons?",
        "Do you use hoppers for sorting?",
        "What's your favorite automatic farm?",
        "Do you build with friends or solo?",
        "What's your favorite multiplayer memory?",
        "Do you play on an SMP?",
        "What's your favorite SMP roleplay?",
        "Do you watch Hermitcraft?",
        "Who's your favorite Hermit?",
        "What's your favorite Minecraft YouTuber?",
        "Do you watch Minecraft tutorials?",
        "What's the best tip you've learned?",
        "What's something you want to learn in Minecraft?",
        "What's your next build project?",
        "What's the biggest build you've done?",
        "Do you do pixel art?",
        "What's your favorite pixel art you've made?",
        "Do you build in different styles?",
        "What's your favorite building style?",
        "Do you use references for builds?",
        "What's your favorite block palette?",
        "Do you use gradients in builds?",
        "What's your favorite roof design?",
        "Do you do interiors?",
        "What's your favorite room to decorate?",
        "Do you use custom NPCs?",
        "What's your favorite datapack?",
        "Do you play with command blocks?",
        "What's the coolest command you've used?",
        "Do you play Minecraft Dungeons?",
        "What's your favorite Minecraft game?",
        "Do you have Minecraft on multiple devices?",
        "What's your favorite way to play?",
        "Do you prefer Java or Bedrock?",
        "What's the biggest difference you notice?",
        "Do you use crossplay?",
        "What's your favorite realm?",
        "Do you host your own server?",
        "What's your favorite plugin?",
        "Do you use mods like OptiFine?",
        "What's your favorite shader pack?",
        "Do you use resource packs?",
        "What's your favorite resource pack?",
        "Do you like the vanilla textures?",
        "What's your favorite block in vanilla?",
        "Do you use the new cherry wood?",
        "What's your favorite new block?",
        "Do you like the bamboo wood set?",
        "What's your favorite wood for building?",
        "Do you use copper in builds?",
        "What's your favorite use for copper?",
        "Do you like the new lightning rod?",
        "What's your favorite use for spyglass?",
        "Do you use goats?",
        "What's your favorite new animal?",
        "Do you like the new frogs?",
        "What's your favorite froglight color?",
        "Do you use tadpoles?",
        "What's your favorite new biome?",
        "Do you like the deep dark?",
        "What's your strategy for ancient cities?",
        "Have you killed the Warden?",
        "What's your favorite new structure?",
        "Do you like trail ruins?",
        "What's your favorite archaeology find?",
        "Do you like the new sniffer?",
        "What's your favorite sniffer plant?",
        "Do you use the new torchflower?",
        "What's your favorite new food?",
        "Do you like the new camel?",
        "What's your favorite way to use camels?",
        "Do you like the new hanging signs?",
        "What's your favorite use for hanging signs?"
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
        "Do you still play the older CODs?",
        "Which COD had the best maps?",
        "What's your favorite map from each game?",
        "Do you like the new MW2?",
        "What's your opinion on the new CODs?",
        "Do you prefer boots on the ground or jetpacks?",
        "Which COD had the best jetpack movement?",
        "What's your favorite exo ability?",
        "Do you like specialists?",
        "Which specialist is your favorite?",
        "Do you prefer pick-10 or classic create-a-class?",
        "What's your favorite wildcard?",
        "Do you use overkill?",
        "What's your favorite perk combination?",
        "Do you use dead silence?",
        "What's your favorite field upgrade?",
        "Do you use trophies?",
        "What's your favorite killstreak to earn?",
        "What's the most satisfying killstreak to use?",
        "Do you like the new killstreak system?",
        "What's your favorite scorestreak from older CODs?",
        "Do you remember the swarm from BO2?",
        "What's your favorite dogs killstreak?",
        "Which game had the best dogs?",
        "Do you like the new gunsmith?",
        "What's your favorite attachment combo?",
        "Do you tune your weapons?",
        "What's your favorite tuning setup?",
        "Do you use different builds for different maps?",
        "What's your favorite weapon for close quarters?",
        "What's your favorite weapon for long range?",
        "Do you have a favorite loadout name?",
        "What's the funniest loadout name you've seen?",
        "Do you use the riot shield?",
        "What's your favorite way to use the riot shield?",
        "Do you use combat axe?",
        "What's your best combat axe kill?",
        "Do you use throwing knives?",
        "What's your best throwing knife kill?",
        "Do you use semtex or frag?",
        "What's your favorite lethal?",
        "Do you use stun or flash?",
        "What's your favorite tactical?",
        "Do you use smoke grenades?",
        "What's your favorite use for smoke?",
        "Do you use heartbeat sensor?",
        "Do you think it's OP?",
        "What's your favorite perk to use in Warzone?",
        "Do you prefer rebirth or regular?",
        "What's your favorite resurgence map?",
        "Do you like Fortune's Keep?",
        "What's your favorite POI in Warzone?",
        "Do you buy UAVs?",
        "What's your favorite killstreak in Warzone?",
        "Do you use self-revives?",
        "What's your favorite way to make money in Warzone?",
        "Do you do contracts? Which ones?",
        "What's your favorite contract type?",
        "Do you use the buy station often?",
        "What's the first thing you buy?",
        "Do you prefer to drive or run?",
        "What's your favorite vehicle in Warzone?",
        "Do you use the gas mask well?",
        "What's your best win in Warzone?",
        "How many Warzone wins do you have?",
        "Do you play solos, duos, trios, or quads?",
        "What's your favorite squad size?",
        "Do you play with the same squad?",
        "What's your best memory in Warzone?"
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
        "Do you sing in the car?",
        "What's your favorite childhood memory?",
        "What was your favorite toy?",
        "What's your favorite thing about today?",
        "What are you looking forward to?",
        "What's something that made you smile today?",
        "What's something you're grateful for?",
        "What's the best thing that happened this week?",
        "What's something you're excited about?",
        "What's a small victory you had recently?",
        "What's a challenge you overcame?",
        "What's something new you tried recently?",
        "What's a goal you have for this month?",
        "What's something you want to achieve this year?",
        "Where do you see yourself in 5 years?",
        "What's your dream job?",
        "If money wasn't an issue, what would you do?",
        "What's your biggest goal right now?",
        "What's something you're working on improving?",
        "What's a habit you want to start?",
        "What's a habit you want to break?",
        "What's your morning routine?",
        "What's your nighttime routine?",
        "Do you make your bed every day?",
        "What's your self-care routine?",
        "How do you relax after a long day?",
        "What do you do to de-stress?",
        "Do you meditate?",
        "Do you exercise regularly?",
        "How many hours of sleep do you need?",
        "Are you a morning person or night owl?",
        "What's your favorite time of day?",
        "Do you prefer weekends or weekdays?",
        "What's your favorite day of the week?",
        "What's your least favorite day?",
        "What's your favorite thing about Monday?",
        "What's your favorite thing about Friday?",
        "Do you have any routines on Sundays?",
        "What's your perfect day off?",
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
        "What's the most beautiful place you've seen?",
        "What's the most peaceful place you've been?",
        "What's the most exciting thing you've done?",
        "What's the most terrifying thing you've done?",
        "What's something that surprised you?",
        "What's something that changed your life?",
        "What's a lesson you learned the hard way?",
        "What's something you wish you knew earlier?",
        "What's your biggest strength?",
        "What's your biggest weakness?",
        "What's something you like about yourself?",
        "What's something you'd like to change?",
        "What makes you happy?",
        "What's your happy place?",
        "What's your love language?",
        "How do you show you care?",
        "How do you like to be comforted?",
        "What do you value most in a friend?",
        "What's the best quality in a person?",
        "What's a red flag in people?",
        "What's something you can't stand?",
        "What's your pet peeve?",
        "What makes you angry?",
        "What makes you sad?",
        "What makes you excited?",
        "Are you introverted or extroverted?",
        "Do you prefer small groups or large crowds?",
        "What's your social battery like?",
        "Do you enjoy meeting new people?",
        "How do you make friends?"
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
        "What's the best game soundtrack to study to?",
        "What's the best game to play with friends?",
        "What's the best game to play alone?",
        "What's a game you've replayed multiple times?",
        "What's a game you'll never play again?",
        "What's the most overpriced game?",
        "What's the best value game?",
        "What's a game that surprised you?",
        "What's a game that disappointed you?",
        "What's your favorite game from last year?",
        "What's your most played game?",
        "How many hours in your favorite game?",
        "Do you have a game you play just to relax?",
        "What's your guilty pleasure game?",
        "What's a game you play that nobody expects?",
        "What's the weirdest game you've played?",
        "What's the most unique game you've played?",
        "What game has the best community?",
        "What game has the worst community?",
        "What's a game that's better than people think?",
        "What's a game that's worse than people think?",
        "What's the best game to play drunk?",
        "What's the best game to play high?",
        "What's the best game to play with kids?",
        "What's the best game to play with non-gamers?",
        "What's the best game to play on a date?",
        "What's the best game to play on a rainy day?",
        "What's the best game to play on a sunny day?",
        "What's the best game to play during the holidays?",
        "What's the best game to play on a weekend?",
        "What's the best game to play on a sick day?",
        "What's the best game to play when you're sad?",
        "What's the best game to play when you're angry?",
        "What's the best game to play when you're bored?",
        "What's the best game to play when you have limited time?",
        "What's the best game to play when you have all day?",
        "What's the best game to play with a controller?",
        "What's the best game to play with keyboard and mouse?",
        "What's the best game to play on a phone?",
        "What's the best game to play on a tablet?",
        "What's the best game to play on a laptop?",
        "What's the best game to play on a console?",
        "What's the best game to play on PC?",
        "What's the best game to play on Nintendo Switch?",
        "What's the best game to play on PlayStation?",
        "What's the best game to play on Xbox?",
        "What's the best cross-platform game?",
        "What's the best game for local multiplayer?",
        "What's the best game for online multiplayer?",
        "What's the best game for co-op?",
        "What's the best game for competitive play?",
        "What's the best game for casual play?",
        "What's the best game for hardcore gamers?",
        "What's the best game for beginners?",
        "What's the best game to get someone into gaming?",
        "What's the best game to play with your parents?",
        "What's the best game to play with your siblings?",
        "What's the best game to play with your kids?",
        "What's the best game to play with your partner?",
        "What's the best game to play with your friends?",
        "What's the best game to play with your online friends?",
        "What's the best game to make new friends?"
    ]
}

# ==================== DATABASE SETUP ====================

async def init_db():
    """Initialize the database tables"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Servers table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS servers (
                guild_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Channels table (for revive channels)
        await db.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                guild_id TEXT,
                channel_id TEXT,
                cooldown_hours INTEGER DEFAULT 2,
                last_message_time TIMESTAMP,
                PRIMARY KEY (guild_id, channel_id)
            )
        ''')
        
        # Custom categories table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS custom_categories (
                guild_id TEXT,
                category_name TEXT,
                PRIMARY KEY (guild_id, category_name)
            )
        ''')
        
        # Custom questions table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS custom_questions (
                guild_id TEXT,
                category_name TEXT,
                question_text TEXT,
                question_index INTEGER,
                PRIMARY KEY (guild_id, category_name, question_index)
            )
        ''')
        
        # Schedules table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                guild_id TEXT,
                channel_id TEXT,
                schedule_time TEXT,  -- Format: "HH:MM"
                PRIMARY KEY (guild_id, channel_id, schedule_time)
            )
        ''')
        
        await db.commit()

async def get_guild_data(guild_id: str) -> Dict[str, Any]:
    """Load all data for a guild from database"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        
        # Get channels
        channels = {}
        async with db.execute(
            "SELECT channel_id, cooldown_hours, last_message_time FROM channels WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            async for row in cursor:
                channels[row['channel_id']] = {
                    'cooldown': row['cooldown_hours'],
                    'last_msg': row['last_message_time'] or datetime.now().isoformat()
                }
        
        # Get custom categories
        custom_cats = []
        async with db.execute(
            "SELECT category_name FROM custom_categories WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            async for row in cursor:
                custom_cats.append(row['category_name'])
        
        # Get custom questions
        custom_questions = {}
        async with db.execute(
            "SELECT category_name, question_text, question_index FROM custom_questions WHERE guild_id = ? ORDER BY question_index",
            (guild_id,)
        ) as cursor:
            async for row in cursor:
                cat = row['category_name']
                if cat not in custom_questions:
                    custom_questions[cat] = []
                custom_questions[cat].append(row['question_text'])
        
        # Get schedules
        schedules = {}
        async with db.execute(
            "SELECT channel_id, schedule_time FROM schedules WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            async for row in cursor:
                ch = row['channel_id']
                if ch not in schedules:
                    schedules[ch] = []
                schedules[ch].append(row['schedule_time'])
        
        return {
            'guild_id': guild_id,
            'channels': channels,
            'custom_categories': custom_cats,
            'custom_questions': custom_questions,
            'schedules': schedules
        }

async def save_channel(guild_id: str, channel_id: int, cooldown: int):
    """Save or update a channel"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR REPLACE INTO channels (guild_id, channel_id, cooldown_hours, last_message_time)
            VALUES (?, ?, ?, ?)
        ''', (guild_id, str(channel_id), cooldown, datetime.now().isoformat()))
        await db.commit()

async def remove_channel(guild_id: str, channel_id: int):
    """Remove a channel"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM channels WHERE guild_id = ? AND channel_id = ?",
            (guild_id, str(channel_id))
        )
        await db.execute(
            "DELETE FROM schedules WHERE guild_id = ? AND channel_id = ?",
            (guild_id, str(channel_id))
        )
        await db.commit()

async def update_last_message(guild_id: str, channel_id: int):
    """Update last message time for a channel"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE channels SET last_message_time = ? WHERE guild_id = ? AND channel_id = ?",
            (datetime.now().isoformat(), guild_id, str(channel_id))
        )
        await db.commit()

async def add_custom_category(guild_id: str, category_name: str):
    """Add a custom category"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO custom_categories (guild_id, category_name) VALUES (?, ?)",
            (guild_id, category_name)
        )
        await db.commit()

async def delete_custom_category(guild_id: str, category_name: str):
    """Delete a custom category and its questions"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM custom_categories WHERE guild_id = ? AND category_name = ?",
            (guild_id, category_name)
        )
        await db.execute(
            "DELETE FROM custom_questions WHERE guild_id = ? AND category_name = ?",
            (guild_id, category_name)
        )
        await db.commit()

async def add_custom_question(guild_id: str, category: str, question: str):
    """Add a custom question"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Get next index
        async with db.execute(
            "SELECT COUNT(*) FROM custom_questions WHERE guild_id = ? AND category_name = ?",
            (guild_id, category)
        ) as cursor:
            count = (await cursor.fetchone())[0]
        
        await db.execute(
            "INSERT INTO custom_questions (guild_id, category_name, question_text, question_index) VALUES (?, ?, ?, ?)",
            (guild_id, category, question, count)
        )
        await db.commit()

async def remove_custom_question(guild_id: str, category: str, index: int):
    """Remove a custom question by index"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM custom_questions WHERE guild_id = ? AND category_name = ? AND question_index = ?",
            (guild_id, category, index)
        )
        await db.commit()

async def add_schedule(guild_id: str, channel_id: int, time_str: str):
    """Add a schedule for a channel"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO schedules (guild_id, channel_id, schedule_time) VALUES (?, ?, ?)",
            (guild_id, str(channel_id), time_str)
        )
        await db.commit()

async def remove_schedule(guild_id: str, channel_id: int, time_str: str):
    """Remove a specific schedule"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM schedules WHERE guild_id = ? AND channel_id = ? AND schedule_time = ?",
            (guild_id, str(channel_id), time_str)
        )
        await db.commit()

async def remove_all_schedules(guild_id: str, channel_id: int = None):
    """Remove all schedules for a channel or guild"""
    async with aiosqlite.connect(DB_PATH) as db:
        if channel_id:
            await db.execute(
                "DELETE FROM schedules WHERE guild_id = ? AND channel_id = ?",
                (guild_id, str(channel_id))
            )
        else:
            await db.execute(
                "DELETE FROM schedules WHERE guild_id = ?",
                (guild_id,)
            )
        await db.commit()

# ==================== UI COMPONENTS ====================

class CategorySelect(discord.ui.Select):
    def __init__(self, bot, guild_data):
        options = [
            discord.SelectOption(
                label=cat.replace('_', ' ').title(),
                value=cat,
                emoji="🔫" if cat == "apex" else "⛏️" if cat == "minecraft" else "💣" if cat == "cod" else "🌍" if cat == "general" else "🎲" if cat == "random" else "📁",
                description=f"{len(DEFAULT_QUESTIONS.get(cat, []))} default questions"
            ) for cat in DEFAULT_QUESTIONS.keys()
        ]
        
        # Add custom categories
        for cat in guild_data.get('custom_categories', []):
            q_count = len(guild_data.get('custom_questions', {}).get(cat, []))
            options.append(
                discord.SelectOption(
                    label=cat.title(),
                    value=f"custom_{cat}",
                    emoji="📌",
                    description=f"{q_count} custom questions"
                )
            )
        
        super().__init__(placeholder="🎯 Choose a category...", min_values=1, max_values=1, options=options)
        self.bot = bot
        self.guild_data = guild_data

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        is_custom = value.startswith("custom_")
        cat_name = value[7:] if is_custom else value
        
        # Store the selected category
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT OR REPLACE INTO channels (guild_id, channel_id, cooldown_hours, last_message_time) VALUES (?, ?, ?, ?)",
                (str(interaction.guild_id), "category_selector", 0, cat_name)
            )
            await db.commit()
        
        embed = discord.Embed(
            title="✅ Category Updated",
            description=f"Now using **{cat_name.title()}** category!",
            color=0x00FF00
        )
        
        # Show example question
        if is_custom:
            questions = self.guild_data.get('custom_questions', {}).get(cat_name, [])
            if questions:
                embed.add_field(name="Example Question", value=f"*{random.choice(questions)}*", inline=False)
        else:
            questions = DEFAULT_QUESTIONS.get(cat_name, [])
            if questions:
                embed.add_field(name="Example Question", value=f"*{random.choice(questions)}*", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class CategoryView(discord.ui.View):
    def __init__(self, bot, guild_data):
        super().__init__(timeout=60)
        self.add_item(CategorySelect(bot, guild_data))

# ==================== BOT CLASS ====================

class ChatPulseBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.check_interval = 60  # Check every 60 seconds
        self.schedule_check_interval = 60  # Check schedules every minute

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Slash commands synced")

    async def on_ready(self):
        print(f'✅ Chat Pulse has connected to Discord!')
        print(f'📊 Bot is in {len(self.guilds)} server(s)')
        print(f'💬 Loaded {sum(len(q) for q in DEFAULT_QUESTIONS.values())} default questions across {len(DEFAULT_QUESTIONS)} categories!')
        
        # Start background tasks
        self.bg_task_inactivity = self.loop.create_task(self.check_inactivity())
        self.bg_task_schedules = self.loop.create_task(self.check_schedules())
        print(f'⏰ Inactivity checker started (checking every {self.check_interval}s)')
        print(f'⏰ Schedule checker started (checking every {self.schedule_check_interval}s)')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Update last message time for tracked channels
        if message.guild:
            await update_last_message(str(message.guild.id), message.channel.id)

    async def check_inactivity(self):
        """Check for inactive channels and send revive questions"""
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                for guild in self.guilds:
                    guild_id = str(guild.id)
                    data = await get_guild_data(guild_id)
                    
                    for channel_id_str, channel_data in data['channels'].items():
                        # Skip the category selector placeholder
                        if channel_id_str == "category_selector":
                            continue
                        
                        channel = self.get_channel(int(channel_id_str))
                        if not channel:
                            continue
                        
                        last_msg_str = channel_data.get('last_msg')
                        if not last_msg_str:
                            continue
                        
                        last_time = datetime.fromisoformat(last_msg_str)
                        time_since = datetime.now() - last_time
                        cooldown = channel_data.get('cooldown', 2)
                        
                        if time_since >= timedelta(hours=cooldown):
                            # Get category for this guild
                            cat_row = None
                            async with aiosqlite.connect(DB_PATH) as db:
                                async with db.execute(
                                    "SELECT last_message_time FROM channels WHERE guild_id = ? AND channel_id = ?",
                                    (guild_id, "category_selector")
                                ) as cursor:
                                    cat_row = await cursor.fetchone()
                            
                            category = cat_row[0] if cat_row else "general"
                            
                            # Get questions (default + custom)
                            questions = []
                            
                            if category in DEFAULT_QUESTIONS:
                                questions.extend(DEFAULT_QUESTIONS[category])
                            
                            if category in data.get('custom_questions', {}):
                                questions.extend(data['custom_questions'][category])
                            
                            if questions:
                                question = random.choice(questions)
                                
                                embed = discord.Embed(
                                    title=f"🌱 Chat's been quiet for {cooldown} hours!",
                                    description=f"**{category.title()} Question:**\n{question}",
                                    color=0x00AAFF
                                )
                                embed.set_footer(text="Chat Pulse • Keeping communities alive")
                                
                                await channel.send(embed=embed)
                                print(f"📤 Inactivity revive in {guild.name}#{channel.name}")
                                
                                # Reset timer
                                await update_last_message(guild_id, channel.id)
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ Error in inactivity checker: {e}")
                traceback.print_exc()
                await asyncio.sleep(self.check_interval)

    async def check_schedules(self):
        """Check for scheduled revives"""
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                
                for guild in self.guilds:
                    guild_id = str(guild.id)
                    data = await get_guild_data(guild_id)
                    
                    for channel_id_str, schedule_times in data['schedules'].items():
                        if current_time in schedule_times:
                            # Check if we already sent this minute (avoid duplicates)
                            last_sent_key = f"last_sent_{channel_id_str}_{current_time}"
                            if hasattr(self, last_sent_key) and getattr(self, last_sent_key) == now.strftime("%Y-%m-%d %H:%M"):
                                continue
                            
                            channel = self.get_channel(int(channel_id_str))
                            if not channel:
                                continue
                            
                            # Get category for this guild
                            cat_row = None
                            async with aiosqlite.connect(DB_PATH) as db:
                                async with db.execute(
                                    "SELECT last_message_time FROM channels WHERE guild_id = ? AND channel_id = ?",
                                    (guild_id, "category_selector")
                                ) as cursor:
                                    cat_row = await cursor.fetchone()
                            
                            category = cat_row[0] if cat_row else "general"
                            
                            # Get questions
                            questions = []
                            if category in DEFAULT_QUESTIONS:
                                questions.extend(DEFAULT_QUESTIONS[category])
                            if category in data.get('custom_questions', {}):
                                questions.extend(data['custom_questions'][category])
                            
                            if questions:
                                question = random.choice(questions)
                                
                                embed = discord.Embed(
                                    title=f"⏰ Scheduled Revive ({current_time})",
                                    description=f"**{category.title()} Question:**\n{question}",
                                    color=0x00AAFF
                                )
                                embed.set_footer(text="Chat Pulse • Daily schedule")
                                
                                await channel.send(embed=embed)
                                print(f"📤 Scheduled revive in {guild.name}#{channel.name} at {current_time}")
                                
                                # Mark as sent
                                setattr(self, last_sent_key, now.strftime("%Y-%m-%d %H:%M"))
                
                await asyncio.sleep(self.schedule_check_interval)
                
            except Exception as e:
                print(f"❌ Error in schedule checker: {e}")
                traceback.print_exc()
                await asyncio.sleep(self.schedule_check_interval)

bot = ChatPulseBot()

# ==================== COMMANDS ====================

@bot.tree.command(name="setup", description="Set up a revive channel")
@app_commands.describe(channel="The channel to revive", hours="Hours of inactivity before revive (default: 2)")
async def setup(interaction: discord.Interaction, channel: discord.TextChannel, hours: int = 2):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    
    # Save channel
    await save_channel(guild_id, channel.id, hours)
    
    embed = discord.Embed(
        title="✅ Channel Setup Complete",
        description=f"📌 **Channel:** {channel.mention}\n⏰ **Cooldown:** {hours} hours",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="addchannel", description="Add another revive channel")
@app_commands.describe(channel="The channel to add", hours="Hours of inactivity before revive (default: 2)")
async def addchannel(interaction: discord.Interaction, channel: discord.TextChannel, hours: int = 2):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    await save_channel(guild_id, channel.id, hours)
    
    embed = discord.Embed(
        title="✅ Channel Added",
        description=f"📌 **Channel:** {channel.mention}\n⏰ **Cooldown:** {hours} hours",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="removechannel", description="Remove a revive channel")
@app_commands.describe(channel="The channel to remove")
async def removechannel(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    await remove_channel(guild_id, channel.id)
    
    embed = discord.Embed(
        title="✅ Channel Removed",
        description=f"📌 **Channel:** {channel.mention} has been removed.",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="listchannels", description="List all revive channels")
async def listchannels(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    data = await get_guild_data(guild_id)
    
    if not data['channels']:
        await interaction.followup.send("❌ No channels set up yet. Use `/setup` to add one.")
        return
    
    embed = discord.Embed(
        title="📋 Revive Channels",
        color=0x00AAFF
    )
    
    for ch_id_str, ch_data in data['channels'].items():
        if ch_id_str == "category_selector":
            continue
        channel = bot.get_channel(int(ch_id_str))
        if channel:
            embed.add_field(
                name=f"#{channel.name}",
                value=f"⏰ Cooldown: {ch_data['cooldown']}h",
                inline=False
            )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="remove", description="Remove ALL setup data for this server")
async def remove_all(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    
    # Delete all data
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM channels WHERE guild_id = ?", (guild_id,))
        await db.execute("DELETE FROM custom_categories WHERE guild_id = ?", (guild_id,))
        await db.execute("DELETE FROM custom_questions WHERE guild_id = ?", (guild_id,))
        await db.execute("DELETE FROM schedules WHERE guild_id = ?", (guild_id,))
        await db.commit()
    
    embed = discord.Embed(
        title="✅ All Data Removed",
        description="All channels, custom categories, questions, and schedules have been deleted.",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="category", description="Choose a question category")
async def category(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    guild_id = str(interaction.guild_id)
    data = await get_guild_data(guild_id)
    
    view = CategoryView(bot, data)
    
    embed = discord.Embed(
        title="🎯 Select Category",
        description="Choose the type of questions you want for your server.",
        color=0x00AAFF
    )
    
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="createcategory", description="Create a custom category")
@app_commands.describe(name="The name of the new category")
async def createcategory(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    
    # Validate name
    if not name.isalnum() and not name.replace('_', '').isalnum():
        await interaction.followup.send("❌ Category name can only contain letters, numbers, and underscores.")
        return
    
    name = name.lower().replace(' ', '_')
    
    await add_custom_category(guild_id, name)
    
    embed = discord.Embed(
        title="✅ Category Created",
        description=f"Category **{name}** has been created! Use `/addquestion` to add questions.",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="deletecategory", description="Delete a custom category")
@app_commands.describe(name="The name of the category to delete")
async def deletecategory(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    name = name.lower().replace(' ', '_')
    
    await delete_custom_category(guild_id, name)
    
    embed = discord.Embed(
        title="✅ Category Deleted",
        description=f"Category **{name}** and all its questions have been deleted.",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="addquestion", description="Add a custom question")
@app_commands.describe(category="The category to add to", question="Your question text")
async def addquestion(interaction: discord.Interaction, category: str, question: str):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    category = category.lower().replace(' ', '_')
    
    await add_custom_question(guild_id, category, question)
    
    embed = discord.Embed(
        title="✅ Question Added",
        description=f"Added to **{category}**:\n*{question}*",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="removequestion", description="Remove a custom question")
@app_commands.describe(category="The category", index="The question number to remove (use /listquestions)")
async def removequestion(interaction: discord.Interaction, category: str, index: int):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    category = category.lower().replace(' ', '_')
    
    await remove_custom_question(guild_id, category, index)
    
    embed = discord.Embed(
        title="✅ Question Removed",
        description=f"Removed question #{index} from **{category}**.",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="listquestions", description="List all questions in a category")
@app_commands.describe(category="The category to list")
async def listquestions(interaction: discord.Interaction, category: str):
    await interaction.response.defer(ephemeral=True)
    
    guild_id = str(interaction.guild_id)
    data = await get_guild_data(guild_id)
    category = category.lower().replace(' ', '_')
    
    embed = discord.Embed(
        title=f"📚 Questions in {category}",
        color=0x00AAFF
    )
    
    # Default questions
    if category in DEFAULT_QUESTIONS:
        default_qs = DEFAULT_QUESTIONS[category][:10]  # Show first 10
        default_text = "\n".join([f"• {q}" for q in default_qs])
        if len(DEFAULT_QUESTIONS[category]) > 10:
            default_text += f"\n*... and {len(DEFAULT_QUESTIONS[category]) - 10} more*"
        embed.add_field(name="📖 Default Questions", value=default_text, inline=False)
    
    # Custom questions
    if category in data.get('custom_questions', {}):
        custom_qs = data['custom_questions'][category]
        if custom_qs:
            custom_text = "\n".join([f"**{i}.** {q}" for i, q in enumerate(custom_qs)])
            embed.add_field(name="✨ Custom Questions", value=custom_text, inline=False)
    
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="schedule_add", description="Add a scheduled revive")
@app_commands.describe(channel="The channel", time="Time in 24h format (e.g., 18:00)")
async def schedule_add(interaction: discord.Interaction, channel: discord.TextChannel, time: str):
    await interaction.response.defer()
    
    # Validate time format
    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        await interaction.followup.send("❌ Invalid time format. Use HH:MM (e.g., 18:00)")
        return
    
    guild_id = str(interaction.guild_id)
    await add_schedule(guild_id, channel.id, time)
    
    embed = discord.Embed(
        title="✅ Schedule Added",
        description=f"📌 **Channel:** {channel.mention}\n⏰ **Time:** {time} daily",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="schedule_remove", description="Remove a scheduled revive")
@app_commands.describe(channel="The channel", time="Time in 24h format (e.g., 18:00)")
async def schedule_remove(interaction: discord.Interaction, channel: discord.TextChannel, time: str):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    await remove_schedule(guild_id, channel.id, time)
    
    embed = discord.Embed(
        title="✅ Schedule Removed",
        description=f"Removed {time} from {channel.mention}",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="schedule_removeall", description="Remove all schedules from a channel")
@app_commands.describe(channel="The channel")
async def schedule_removeall(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    await remove_all_schedules(guild_id, channel.id)
    
    embed = discord.Embed(
        title="✅ All Schedules Removed",
        description=f"All schedules removed from {channel.mention}",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="schedule_list", description="List all schedules")
@app_commands.describe(channel="Optional: filter by channel")
async def schedule_list(interaction: discord.Interaction, channel: discord.TextChannel = None):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    data = await get_guild_data(guild_id)
    
    embed = discord.Embed(
        title="📋 Scheduled Revives",
        color=0x00AAFF
    )
    
    if channel:
        ch_id = str(channel.id)
        if ch_id in data['schedules'] and data['schedules'][ch_id]:
            times = ", ".join(data['schedules'][ch_id])
            embed.add_field(name=channel.mention, value=f"⏰ {times}", inline=False)
        else:
            embed.description = f"No schedules for {channel.mention}"
    else:
        for ch_id_str, times in data['schedules'].items():
            if times:
                channel_obj = bot.get_channel(int(ch_id_str))
                if channel_obj:
                    times_str = ", ".join(times)
                    embed.add_field(name=f"#{channel_obj.name}", value=f"⏰ {times_str}", inline=False)
        
        if not embed.fields:
            embed.description = "No schedules set up yet."
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="revive", description="Manually trigger a revive question")
@app_commands.describe(channel="Optional: specific channel (defaults to current)")
async def revive(interaction: discord.Interaction, channel: discord.TextChannel = None):
    await interaction.response.defer()
    
    target_channel = channel or interaction.channel
    guild_id = str(interaction.guild_id)
    
    # Get category
    cat_row = None
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT last_message_time FROM channels WHERE guild_id = ? AND channel_id = ?",
            (guild_id, "category_selector")
        ) as cursor:
            cat_row = await cursor.fetchone()
    
    category = cat_row[0] if cat_row else "general"
    data = await get_guild_data(guild_id)
    
    # Get questions
    questions = []
    if category in DEFAULT_QUESTIONS:
        questions.extend(DEFAULT_QUESTIONS[category])
    if category in data.get('custom_questions', {}):
        questions.extend(data['custom_questions'][category])
    
    if not questions:
        await interaction.followup.send("❌ No questions found for this category.")
        return
    
    question = random.choice(questions)
    
    embed = discord.Embed(
        title="🔄 Manual Revive",
        description=f"**{category.title()} Question:**\n{question}",
        color=0x00AAFF
    )
    
    await target_channel.send(embed=embed)
    await interaction.followup.send(f"✅ Sent revive to {target_channel.mention}", ephemeral=True)
    
    # Reset timer if it's a tracked channel
    await update_last_message(guild_id, target_channel.id)

@bot.tree.command(name="status", description="Check chat activity")
@app_commands.describe(channel="Optional: specific channel (defaults to current)")
async def status(interaction: discord.Interaction, channel: discord.TextChannel = None):
    await interaction.response.defer()
    
    target_channel = channel or interaction.channel
    guild_id = str(interaction.guild_id)
    
    # Get channel data
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        async with db.execute(
            "SELECT cooldown_hours, last_message_time FROM channels WHERE guild_id = ? AND channel_id = ?",
            (guild_id, str(target_channel.id))
        ) as cursor:
            row = await cursor.fetchone()
    
    if not row:
        await interaction.followup.send(f"❌ {target_channel.mention} is not set up as a revive channel.")
        return
    
    last_time = datetime.fromisoformat(row['last_message_time'])
    time_since = datetime.now() - last_time
    hours = int(time_since.total_seconds() / 3600)
    minutes = int((time_since.total_seconds() / 60) % 60)
    
    # Get category
    async with db.execute(
        "SELECT last_message_time FROM channels WHERE guild_id = ? AND channel_id = ?",
        (guild_id, "category_selector")
    ) as cursor:
        cat_row = await cursor.fetchone()
    
    category = cat_row[0] if cat_row else "general"
    
    embed = discord.Embed(
        title="📊 Channel Status",
        description=f"📌 **Channel:** {target_channel.mention}\n"
                   f"🗂️ **Category:** {category.title()}\n"
                   f"⏰ **Cooldown:** {row['cooldown_hours']} hours\n"
                   f"💬 **Last Message:** {hours}h {minutes}m ago",
        color=0x00AAFF
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="cooldown", description="Change cooldown for a channel")
@app_commands.describe(hours="Hours of inactivity (1-12)", channel="Optional: specific channel (defaults to current)")
async def cooldown(interaction: discord.Interaction, hours: int, channel: discord.TextChannel = None):
    await interaction.response.defer()
    
    if hours < 1 or hours > 12:
        await interaction.followup.send("❌ Cooldown must be between 1 and 12 hours.")
        return
    
    target_channel = channel or interaction.channel
    guild_id = str(interaction.guild_id)
    
    # Update cooldown
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE channels SET cooldown_hours = ? WHERE guild_id = ? AND channel_id = ?",
            (hours, guild_id, str(target_channel.id))
        )
        await db.commit()
    
    embed = discord.Embed(
        title="✅ Cooldown Updated",
        description=f"📌 **Channel:** {target_channel.mention}\n⏰ **New Cooldown:** {hours} hours",
        color=0x00FF00
    )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="settings", description="View all server settings")
async def settings(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild_id = str(interaction.guild_id)
    data = await get_guild_data(guild_id)
    
    embed = discord.Embed(
        title="⚙️ Server Settings",
        color=0x00AAFF
    )
    
    # Get category
    cat_row = None
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT last_message_time FROM channels WHERE guild_id = ? AND channel_id = ?",
            (guild_id, "category_selector")
        ) as cursor:
            cat_row = await cursor.fetchone()
    
    category = cat_row[0] if cat_row else "general"
    embed.add_field(name="🗂️ Current Category", value=category.title(), inline=False)
    
    # Channels
    channels_list = []
    for ch_id_str, ch_data in data['channels'].items():
        if ch_id_str != "category_selector":
            channel = bot.get_channel(int(ch_id_str))
            if channel:
                channels_list.append(f"#{channel.name} ({ch_data['cooldown']}h)")
    
    if channels_list:
        embed.add_field(name="📌 Revive Channels", value="\n".join(channels_list), inline=False)
    else:
        embed.add_field(name="📌 Revive Channels", value="None set up", inline=False)
    
    # Custom categories
    if data['custom_categories']:
        embed.add_field(name="📁 Custom Categories", value=", ".join(data['custom_categories']), inline=False)
    
    # Schedules
    schedule_count = sum(len(times) for times in data['schedules'].values())
    embed.add_field(name="⏰ Schedules", value=f"{schedule_count} active", inline=False)
    
    # Custom questions count
    custom_q_count = sum(len(qs) for qs in data['custom_questions'].values())
    embed.add_field(name="✨ Custom Questions", value=f"{custom_q_count} total", inline=False)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 **Pong!** Latency: `{latency}ms`")

@bot.tree.command(name="stats", description="Show bot statistics")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer()
    
    # Count servers
    server_count = len(bot.guilds)
    
    # Count total questions
    default_q_count = sum(len(q) for q in DEFAULT_QUESTIONS.values())
    
    # Count custom questions from DB
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM custom_questions") as cursor:
            custom_q_count = (await cursor.fetchone())[0]
    
    # Count schedules
    async with db.execute("SELECT COUNT(*) FROM schedules") as cursor:
        schedule_count = (await cursor.fetchone())[0]
    
    embed = discord.Embed(
        title="📊 Chat Pulse Statistics",
        color=0x00AAFF
    )
    
    embed.add_field(name="🖥️ Servers", value=str(server_count), inline=True)
    embed.add_field(name="📚 Default Questions", value=str(default_q_count), inline=True)
    embed.add_field(name="✨ Custom Questions", value=str(custom_q_count), inline=True)
    embed.add_field(name="⏰ Active Schedules", value=str(schedule_count), inline=True)
    embed.add_field(name="🗂️ Categories", value=str(len(DEFAULT_QUESTIONS)), inline=True)
    embed.add_field(name="💎 Version", value="Ultimate 2.0", inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="donate", description="Support Chat Pulse development")
async def donate(interaction: discord.Interaction):
    embed = discord.Embed(
        title="☕ Support Chat Pulse",
        description="Love the bot? Consider supporting!\n\n"
                   "[💰 Buy Me a Coffee](https://buymeacoffee.com/YOUR_USERNAME)\n"
                   "[❤️ Become a Patron](https://patreon.com/YOUR_USERNAME)",
        color=0x00AAFF
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="vote", description="Vote for Chat Pulse")
async def vote(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🗳️ Vote for Chat Pulse",
        description="Support the bot by voting!\n\n"
                   "[🔗 Vote on top.gg](https://top.gg/bot/YOUR_BOT_ID)",
        color=0x00AAFF
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="feedback", description="Send feedback to the developer")
@app_commands.describe(message="Your feedback or suggestion")
async def feedback(interaction: discord.Interaction, message: str):
    # Log to console (you can add a webhook later)
    print(f"📝 FEEDBACK from {interaction.user} ({interaction.user.id}) in {interaction.guild}: {message}")
    
    embed = discord.Embed(
        title="✅ Feedback Sent",
        description="Thank you! Your feedback has been sent to the developer.",
        color=0x00FF00
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Chat Pulse - Ultimate Revival Bot",
        description="Keep your community alive with auto-revive questions!",
        color=0x00AAFF
    )
    
    embed.add_field(
        name="📝 **Setup Commands**",
        value=(
            "`/setup #channel [hours]` - Set revive channel\n"
            "`/addchannel #channel [hours]` - Add another\n"
            "`/removechannel #channel` - Remove channel\n"
            "`/listchannels` - Show all channels\n"
            "`/remove` - Delete ALL data"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 **Category Commands**",
        value=(
            "`/category` - Choose category\n"
            "`/createcategory [name]` - Create custom\n"
            "`/deletecategory [name]` - Delete custom\n"
            "`/addquestion [category] [text]` - Add question\n"
            "`/removequestion [category] [index]` - Remove\n"
            "`/listquestions [category]` - List questions"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⏰ **Schedule Commands**",
        value=(
            "`/schedule_add #channel HH:MM` - Add schedule\n"
            "`/schedule_remove #channel HH:MM` - Remove\n"
            "`/schedule_removeall #channel` - Remove all\n"
            "`/schedule_list [#channel]` - List schedules"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚡ **Action Commands**",
        value=(
            "`/revive [#channel]` - Manual revive\n"
            "`/status [#channel]` - Check activity\n"
            "`/cooldown [hours] [#channel]` - Change cooldown\n"
            "`/settings` - View all settings"
        ),
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ **Info Commands**",
        value=(
            "`/ping` - Check latency\n"
            "`/stats` - Bot statistics\n"
            "`/donate` - Support development\n"
            "`/vote` - Vote for the bot\n"
            "`/feedback` - Send suggestions\n"
            "`/help` - Show this menu"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 **Default Categories**",
        value=(
            f"🔫 **Apex:** {len(DEFAULT_QUESTIONS['apex'])} questions\n"
            f"⛏️ **Minecraft:** {len(DEFAULT_QUESTIONS['minecraft'])} questions\n"
            f"💣 **COD:** {len(DEFAULT_QUESTIONS['cod'])} questions\n"
            f"🌍 **General:** {len(DEFAULT_QUESTIONS['general'])} questions\n"
            f"🎲 **Random:** {len(DEFAULT_QUESTIONS['random'])} questions\n"
            f"✨ **Total:** {sum(len(q) for q in DEFAULT_QUESTIONS.values())}+ questions"
        ),
        inline=False
    )
    
    embed.set_footer(text="Chat Pulse • Keeping communities alive • 100% Free Forever")
    
    await interaction.response.send_message(embed=embed)

# ==================== RUN BOT ====================

async def main():
    await init_db()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
