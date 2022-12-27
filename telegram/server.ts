import "dotenv/config";

import { InlineQueryResult, InlineQueryResultGame } from "telegraf/types";
import { Markup, Telegraf } from "telegraf";

import { addDiceGame } from "./games/dice";
import express from "express";

const { message } = require("telegraf/filters");

const PORT = process.env.PORT;
const TELEGRAM_API_KEY = process.env.TELEGRAM_API_KEY
  ? process.env.TELEGRAM_API_KEY
  : "";
const bot = new Telegraf(TELEGRAM_API_KEY);
const app = express();

// Set the bot API endpoint
// app.use(await bot.createWebhook({ domain: "localhost:3000" }));

bot.start((ctx) => ctx.reply("Welcome"));
bot.help((ctx) => ctx.reply("Send me a sticker"));
bot.hears("hi", (ctx) => ctx.reply("Hey there"));

addDiceGame(bot);

let games: { game_short_name: string }[] = [{ game_short_name: "dice" }];

bot.on("inline_query", async (ctx) => {
  const markup = Markup.inlineKeyboard([Markup.button.game("🎮 Play now!")]);

  const gamess = (games as { game_short_name: string }[])
    .filter(({ game_short_name }) => game_short_name)
    .map(
      ({ game_short_name }): InlineQueryResultGame => ({
        type: "game",
        id: game_short_name,
        game_short_name: "dice",
        ...Markup.inlineKeyboard([Markup.button.game("🎮 Play now!")]),
      })
    );
  return await ctx.answerInlineQuery(gamess);
});

bot.launch();

app.listen(PORT, () => console.log("Listening on PORT", PORT));

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
