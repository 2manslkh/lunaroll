const Moralis = require("moralis").default;
const { ethers } = require("ethers");
const { response } = require("../server");

require("dotenv").config();
Moralis.start({
  apiKey: process.env.MORALIS_KEY,
});
async function getWalletArgonautNFTs(address) {
  let cursor = null;
  let nfts = [];
  let response;
  do {
    response = await Moralis.EvmApi.nft.getWalletNFTs({
      address: address,
      chain: "0x19", // CRONOS MAINNET
      tokenAddresses: ["0xa996aD2b9f240F78b063E47F552037658c4563d1"],
      cursor: cursor,
    });
    for (const nft of response.result) {
      nfts.push(nft);
    }
    cursor = response.data.cursor;
  } while (cursor != "" && cursor != null);
  return nfts;
}

// async function getWalletArgonautNFTs(address) {
//   let results;
//   // Recursion Loop
//   async function _getWalletArgonautNFTs(address, results, cursor) {
//     if (cursor === null) {
//       return results;
//     } else {
//       let response = await Moralis.EvmApi.nft.getWalletNFTs({
//         address: address,
//         cursor: cursor,
//         chain: "0x19", // CRONOS MAINNET
//         tokenAddresses: ["0xa996aD2b9f240F78b063E47F552037658c4563d1"],
//       });
//       if (!results) {
//         results = response;
//       } else {
//         results.result = results.result.concat(response.data.result);
//       }
//       return await _getWalletArgonautNFTs(
//         address,
//         results,
//         response.data.cursor
//       );
//     }
//   }

//   return (await _getWalletArgonautNFTs(address, results, 0)).result;
// }

async function getWalletArgonautNFTsCount(address) {
  // Recursion Loop
  try {
    let response = await Moralis.EvmApi.nft.getWalletNFTs({
      address: address,
      chain: "0x19", // CRONOS MAINNET
      tokenAddresses: ["0xa996aD2b9f240F78b063E47F552037658c4563d1"],
    });
    // console.log("🚀 | getWalletArgonautNFTsCount | response", response);
    return response.data.total;
  } catch (error) {
    console.log(error);
    throw error;
  }
}

async function getWalletERC20Balance(userAddress, tokenAddress) {
  try {
    let response = await Moralis.EvmApi.token.getWalletTokenBalances({
      address: userAddress,
      chain: "0x19", // CRONOS MAINNET
      tokenAddresses: [tokenAddress],
    });
    return ethers.utils.parseEther(response.data[0].balance);
  } catch (error) {
    console.log(error);
    throw error;
  }
}

module.exports = {
  getWalletArgonautNFTs,
  getWalletERC20Balance,
  getWalletArgonautNFTsCount,
};
