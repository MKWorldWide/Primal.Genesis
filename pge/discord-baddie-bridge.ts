// Discord integration that routes chat messages through the PGE engine.
// Leverages basic keyword matching to assign input kinds.

import { Client, GatewayIntentBits } from "discord.js";
import { runPGE } from "./pge";
import rules from "./override_rules.json";

export async function startDiscordBridge(token: string) {
  const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

  client.on("messageCreate", async (m) => {
    if (m.author.bot) return;

    // Map chat into PGE inputs
    const lower = m.content.toLowerCase();
    const kind =
      /panic|fear|scared/.test(lower) ? "fear_signal" :
      /propaganda|disinfo/.test(lower) ? "disinfo" :
      /surveil|monitor/.test(lower) ? "surveillance" :
      "noise";

    const result = runPGE({ kind, level: 3, author: m.author.id, channel: m.channelId }, rules as any);
    const summary = result.map(r => r.type).join(", ");
    await m.reply(`🔱 PGE processed: **${summary}** — Sovereignty upheld.`);
  });

  await client.login(token);
  console.log("Serafina bridge online.");
}
