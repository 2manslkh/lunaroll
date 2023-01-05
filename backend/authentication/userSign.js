// Prove that incoming address is the owner

const { ethers } = require("ethers");

// Initialize Domain
const domain = {
  name: "Atlantis",
  version: "1",
  chainId: 25, // mainnet = 25, testnet = 338
};

// The named list of all type definitions
const types = {
  Claim: [
    { name: "item_name", type: "string" },
    { name: "amount", type: "uint256" },
  ],
};

/**
 * Verify the signature of a cheese claim // TODO: Generalize this to any claim
 * @param {string} address
 * @param {string} signature
 * @param {string} data
 * @returns
 */
function verifyTypedSignature(address, signature, data) {
  return (
    address ===
    ethers.utils.verifyTypedData(
      {
        name: "Atlantis",
        version: "1",
        chainId: 25, // mainnet = 25, testnet = 338
      },
      {
        Claim: [
          { name: "item_name", type: "string" },
          { name: "amount", type: "uint256" },
        ],
      },
      { item_name: data.item_name, amount: data.amount },
      signature
    )
  );
}

/**
 * Verify the signature of a cheese claim // TODO: Generalize this to any claim
 * @param {string} address
 * @param {string} signature
 * @param {Object} data
 * @returns
 */
function verifyCheckin(address, signature, data) {
  return (
    address ===
    ethers.utils.verifyTypedData(
      {
        name: "Odyssey",
        version: "1",
        chainId: 25, // mainnet = 25, testnet = 338
      },
      {
        Checkin: [{ name: "taskNumber", type: "string" }],
      },
      { taskNumber: data.taskNumber },
      signature
    )
  );
}

module.exports = { verifyTypedSignature, verifyCheckin };
