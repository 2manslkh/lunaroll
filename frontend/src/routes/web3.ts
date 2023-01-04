import { EthereumClient, modalConnectors, walletConnectProvider } from '@web3modal/ethereum';
import { configureChains, createClient } from '@wagmi/core';
import { goerli, mainnet } from '@wagmi/core/chains';

import { Web3Modal } from '@web3modal/html';

//  1. Define constants
const projectId = '8e6b5ffdcbc9794bf9f4a1952578365b';
const chains = [mainnet, goerli];

// 2. Configure wagmi client
const { provider } = configureChains(chains, [walletConnectProvider({ projectId })]);
export const client = createClient({
	autoConnect: true,
	connectors: modalConnectors({ appName: 'web3Modal', chains }),
	provider
});

// 3. Create ethereum and modal clients
export const ethereumClient = new EthereumClient(client, chains);
export const web3Modal = new Web3Modal({ projectId }, ethereumClient);
