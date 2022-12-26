import "dotenv/config";

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

bot.launch();

app.listen(PORT, () => console.log("Listening on PORT", PORT));

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
