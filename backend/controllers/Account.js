const { ethers } = require("ethers");
const { verifyTypedSignature } = require("../authentication/userSign");

require("dotenv").config();

const MNEMONIC = process.env.MNEMONIC;

/**
 * Withdraw Request Payload
 * @typedef {object} WithdrawRequestPayload
 * @property {string} telegramId.required
 * @property {string} withdrawAddress.required
 * @property {string} currency.required
 * @property {string} amount.required
 */

/**
 * Create Account Request Payload
 * @typedef {object} CreateAccountPayload
 * @property {string} telegramId.required
 */

/**
 * Reward Redeemed Response
 * @typedef {object} DefaultSuccessResponse
 * @property {string} message.required - Message of the response
 */

/**
 * Reward Redeemed Response
 * @typedef {object} DefaultErrorResponse
 * @property {string} message.required - Message of the response
 */

/**
 * GET /account/getBalance
 * @summary Get Balance of Account
 * @tags Account
 * @description Get Balance of Account
 * @param {string} telegramId.query.required - Telegram ID of the user
 * @return {DefaultSuccessResponse} 200 - Success response
 * @return {DefaultErrorResponse} 400 - Bad request response
 */
exports.getBalance = async (req, res, next) => {
  // Get query parameters
  const { telegramId } = req.query;
  // Return Balance of user
  return res.status(200).json({
    telegramId,
    balances: { USDT: "1000" },
  });
};

/**
 * GET /account/getDepositAddress
 * @summary Get Deposit Address of Account
 * @tags Account
 * @description Get Balance of Account
 * @param {string} telegramId.query.required - Telegram ID of the user
 * @return {DefaultSuccessResponse} 200 - Success response
 * @return {DefaultErrorResponse} 400 - Bad request response
 */
exports.getDepositAddress = async (req, res, next) => {
  // Get query parameters
  const { telegramId } = req.query;

  try {
    wallet = getWalletFromTelegramId(telegramId);
  } catch (error) {
    console.log("🚀 | exports.create= | error", error);
    return res.status(400).json({
      success: false,
      message: "Error creating wallet",
    });
  }

  // Return Wallet Address of user
  return res.status(200).json({
    telegramId,
    depositAddress: wallet.address,
  });
};

/**
 * POST /account/withdraw
 * @summary Withdraw Crypto
 * @tags Account
 * @description Withdraw Crypto from user's balance
 * @param {WithdrawRequestPayload} request.body.required - Address of the user
 * @return {DefaultSuccessResponse} 200 - Success response
 * @return {DefaultErrorResponse} 400 - Bad request response
 */
exports.withdraw = async (req, res, next) => {
  const { telegramId, withdrawAddress, currency, amount } = req.body;
  // Withdraw Crypto from user's balance
  return res.status(200).json({
    success: true,
    telegramId,
    withdrawAddress,
    currency,
    amount,
  });
};

/**
 * POST /account/create
 * @summary Create new custodial wallet
 * @tags Account
 * @description Create new custodial wallet from user's telegram id
 * @param {CreateAccountPayload} request.body.required - Address of the user
 * @return {DefaultSuccessResponse} 200 - Success response
 * @return {DefaultErrorResponse} 400 - Bad request response
 */
exports.create = async (req, res, next) => {
  const { telegramId } = req.body;

  // Convert telegram ID to BigNumber

  let wallet;

  try {
    wallet = getWalletFromTelegramId(telegramId);
  } catch (error) {
    console.log("🚀 | exports.create= | error", error);
    return res.status(400).json({
      success: false,
      message: "Error creating wallet",
    });
  }

  // Return Wallet Address
  return res.status(200).json({
    success: true,
    address: wallet.address,
  });
};
function getWalletFromTelegramId(telegramId) {
  const telegramIdBigNumber = ethers.BigNumber.from(telegramId);
  // Divide telegram ID by 2147483647
  const telegramIdDivided = telegramIdBigNumber.div(2147483647);
  // Get the remainder of telegram ID divided by 2147483647
  const telegramIdRemainder = telegramIdBigNumber.mod(2147483647);
  // Convert both to string
  const telegramIdDividedString = telegramIdDivided.toString();
  const telegramIdString = telegramIdRemainder.toString();
  const wallet = ethers.Wallet.fromMnemonic(
    MNEMONIC,
    `m/44'/60'/0'/${telegramIdDividedString}/${telegramIdString}`
  );
  return wallet;
}
