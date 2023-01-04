<script>
	import { page } from '$app/stores';
	import logo from '$lib/images/LUNAR_ROLL_header.svg';
	import github from '$lib/images/github.svg';

	import { configureChains, createClient } from '@wagmi/core'
	import { goerli, mainnet } from '@wagmi/core/chains'
	import { EthereumClient, modalConnectors, walletConnectProvider } from '@web3modal/ethereum'
	import { Web3Modal } from '@web3modal/html'

	// // 1. Define constants
	const projectId = '8e6b5ffdcbc9794bf9f4a1952578365b'
	const chains = [mainnet, goerli]

	// // // 2. Configure wagmi client
	const { provider } = configureChains(chains, [walletConnectProvider({ projectId })])
	const wagmiClient = createClient({
	autoConnect: true,
	connectors: modalConnectors({ appName: 'web3Modal', chains }),
	provider
	})

	// // // 3. Create ethereum and modal clients
	const ethereumClient = new EthereumClient(wagmiClient, chains)
	export const web3Modal = new Web3Modal({ projectId }, ethereumClient)
</script>

<header>
	<div class="header-logo">
		<img src={logo} alt="LunarRoll" />
		<w3m-network-switch></w3m-network-switch>
		<w3m-core-button></w3m-core-button>
	</div>
</header>

<style>
	header {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.header-logo {
		padding: 32px;
		width: 50%;
	}
	.header-logo img {
		/* padding: 10px; */
		width: 100%;
	}
</style>
