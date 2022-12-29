import "dotenv/config";

import { Context, Markup, Scenes, Telegraf, session } from "telegraf";
import { InlineQueryResultGame, Message } from "telegraf/types";

import { LunarollContext } from "./context";
import { addDiceGame } from "./games/dice";
import express from "express";
import { message } from "telegraf/filters";

var QRCode = require("qrcode");

const PORT = process.env.PORT;
const TELEGRAM_API_KEY = process.env.TELEGRAM_API_KEY
  ? process.env.TELEGRAM_API_KEY
  : "";

// Set the bot API endpoint
// app.use(await bot.createWebhook({ domain: "localhost:3000" }));

// Scenes

// Handler factories

/**
 * We can define our own context object.
 *
 * We have to set the scene object under the `scene` property.
 */

// Greeter scene
// const withdrawScene = new Scenes.BaseScene<LunarollContext>("withdraw");
// withdrawScene.enter((ctx) =>
//   ctx.reply("Balances:\n\nUSDT: 1000.00", WITHDRAW_IK())
// );

// withdrawScene.action("withdraw_usdt", (ctx) => {
//   ctx.tokenAddress = "USDT";
//   ctx.scene.enter("withdraw_amount", ctx.reply("USDT"));
// });

// const withdrawAmountScene = new Scenes.BaseScene<LunarollContext>(
//   "withdraw_amount"
// );
// withdrawAmountScene.enter((ctx) => {
//   console.log(ctx.tokenAddress);
//   ctx.reply("Amount of USDT to withdraw:");
// });

// withdrawAmountScene.on(message("text"), (ctx) => {
//   console.log("🚀 | withdrawAmountScene.on | ctx", ctx);
//   // Perform regex on message to make sure it's a number
//   const text = ctx.message.text;
//   const regex = /^\d+(\.\d{1,5})?$/;
//   if (!regex.test(text)) {
//     ctx.reply("Please enter a valid amount");
//   } else {
//     ctx.amount = text;
//     console.log(ctx.tokenAddress);

//     ctx.reply(`Withdraw ${ctx.amount} ${ctx.tokenAddress}`);
//     ctx.scene.enter("withdraw_address");
//   }
// });

// const withdrawAddressScene = new Scenes.BaseScene<LunarollContext>(
//   "withdraw_address"
// );
// withdrawAddressScene.enter((ctx) => ctx.reply("Withdrawal Address:"));

// withdrawAddressScene.on(message("text"), (ctx) => {
//   // Perform regex on message to make sure it's a number
//   const text = ctx.message.text;
//   const regex = /^0x[0-9a-fA-F]{40}$/;
//   if (!regex.test(text)) {
//     ctx.reply("Please enter a valid address");
//   } else {
//     ctx.amount = text;
//     ctx.reply(
//       `Withdraw ${ctx.amount} ${ctx.tokenAddress} to ${ctx.withdrawAddress}?`,
//       CONFIRMATION_IK()
//     );
//     ctx.scene.enter("withdraw_address");
//   }
// });

const withdrawWizard = new Scenes.WizardScene<LunarollContext>(
  "withdraw_wizard",
  async (ctx) => {
    await ctx.reply("Balances:\n\nUSDT: 1000.00", WITHDRAW_IK());
    return ctx.wizard.next();
  },
  async (ctx) => {
    await ctx.reply("Currency to withdraw:");
    return ctx.wizard.next();
  },
  async (ctx) => {
    await ctx.reply("Amount of USDT to withdraw:");

    return ctx.wizard.next();
  },
  async (ctx) => {
    await ctx.reply("Address to withdraw to:");

    return await ctx.scene.leave();
  }
);

// const withdrawWizard = new Scenes.WizardScene(
//   'withdraw_wizard', // first argument is Scene_ID, same as for BaseScene
//   (ctx) => {
//     ctx.reply('What is your name?');
//     ctx.wizard.state.contactData = {};
//     return ctx.wizard.next();
//   },
//   (ctx) => {
//     // validation example
//     if (ctx.message.text.length < 2) {
//       ctx.reply('Please enter name for real');
//       return;
//     }
//     ctx.wizard.state.contactData.fio = ctx.message.text;
//     ctx.reply('Enter your e-mail');
//     return ctx.wizard.next();
//   },
//   async (ctx) => {
//     ctx.wizard.state.contactData.email = ctx.message.text;
//     ctx.reply('Thank you for your replies, we'll contact your soon');
//     await mySendContactDataMomentBeforeErase(ctx.wizard.state.contactData);
//     return ctx.scene.leave();
//   },
// );

// Define the callback functions for the buttons
const callback1 = (ctx: Context) => console.log("Button 1 pressed");
const callback2 = (ctx: Context) => ctx.reply("Button 2 pressed");
const callback3 = (ctx: Context) => ctx.reply("Button 3 pressed");

// Create the inline keyboard
const MAIN_MENU_IK = () =>
  Markup.keyboard([["📝 Register", "💰 Deposit", "💸 Withdraw"]])
    .oneTime()
    .resize();

const WITHDRAW_IK = () =>
  Markup.inlineKeyboard([[Markup.button.callback("USDT", "withdraw_usdt")]]);

const CONFIRMATION_IK = () =>
  Markup.inlineKeyboard([
    [Markup.button.callback("Yes", "withdraw_confirm")],
    [Markup.button.callback("No", "withdraw_cancel")],
  ]);

const bot = new Telegraf<LunarollContext>(TELEGRAM_API_KEY);
const app = express();

// Set up the handler for the inline keyboard
// bot.action("withdraw_usdt", callback1);
bot.action("button2", callback2);
bot.action("button3", callback3);

const stage = new Scenes.Stage<LunarollContext>([withdrawWizard], {
  // default: "super-wizard",
});

bot.use(session());
bot.use(stage.middleware());

// bot.use((ctx, next) => {
//   // we now have access to the the fields defined above
//   ctx.amount ??= "";
//   ctx.tokenAddress ??= "";
//   ctx.withdrawAddress ??= "";

//   return next();
// });

bot.start((ctx) => ctx.reply("Welcome", MAIN_MENU_IK()));
bot.help((ctx) => ctx.reply("Send me a sticker"));

bot.hears("hi", (ctx) => ctx.reply(ctx.message.text));
bot.hears("📝 Register", (ctx) => ctx.reply("register"));
bot.hears("💰 Deposit", (ctx) => {
  ctx.reply("Your Deposit Address: 0xCa5cF03D081197BE24eF707081FbD7F3F11EB02D");
  QRCode.toDataURL(
    "0xCa5cF03D081197BE24eF707081FbD7F3F11EB02D",
    function (err: any, url: any) {
      ctx.replyWithPhoto({
        source: Buffer.from(url.split(",")[1], "base64"),
      });
    }
  );
});
bot.hears("💸 Withdraw", (ctx) => ctx.scene.enter("withdraw_wizard"));

addDiceGame(bot);

let games: { game_short_name: string }[] = [{ game_short_name: "dice" }];

bot.on("inline_query", async (ctx) => {
  const gamesList = (games as { game_short_name: string }[])
    .filter(({ game_short_name }) => game_short_name)
    .map(
      ({ game_short_name }): InlineQueryResultGame => ({
        type: "game",
        id: game_short_name,
        game_short_name: "dice",
        ...Markup.inlineKeyboard([Markup.button.game("🎮 Play now!")]),
      })
    );
  return await ctx.answerInlineQuery(gamesList);
});

bot.launch();

app.listen(PORT, () => console.log("Listening on PORT", PORT));

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
