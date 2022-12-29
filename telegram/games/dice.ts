import { Context, Markup, Scenes, Telegraf } from "telegraf";

import { LunarollContext } from "../context";
const FRONTEND_BASE_URL = process.env.FRONTEND_BASE_URL || "";

export function addDiceGame(bot: Telegraf<LunarollContext>) {
  const gameShortName = "dice";
  const gameUrl = FRONTEND_BASE_URL;
  console.log("🚀 | addDiceGame | gameUrl", gameUrl);

  const markup = Markup.inlineKeyboard([Markup.button.game("🎮 Play now!")]);

  bot.command("dice", (ctx) => ctx.replyWithGame(gameShortName, markup));
  bot.gameQuery((ctx) => ctx.answerGameQuery(gameUrl));
}
