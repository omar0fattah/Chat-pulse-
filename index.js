const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

const TOKEN = process.env.DISCORD_TOKEN;
const reviveThresholdMs = 48 * 60 * 60 * 1000; // 48 hours
const lastSeen = new Map();

client.on('ready', () => {
  console.log(`Ready as ${client.user.tag}`);
  // initial populate
  client.guilds.cache.forEach(g => g.channels.cache.filter(c => c.isTextBased()).forEach(ch => lastSeen.set(ch.id, Date.now())));
  setInterval(checkChannels, 30 * 60 * 1000); // every 30 minutes
});

client.on('messageCreate', msg => {
  if (msg.author.bot) return;
  lastSeen.set(msg.channel.id, Date.now());
});

async function checkChannels() {
  for (const [id, ts] of lastSeen) {
    const ch = await client.channels.fetch(id).catch(()=>null);
    if (!ch || !ch.isTextBased()) continue;
    const idle = Date.now() - ts;
    if (idle > reviveThresholdMs) {
      ch.send("Hey everyone — bump! Anyone around?"); // customize
      lastSeen.set(id, Date.now());
    }
  }
}

client.login(TOKEN);
