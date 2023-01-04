<script>
	import { ethers } from 'ethers';
	import abi from '../../lib/contracts/WETH.json';
	console.log('🚀 | abi', abi);

	import { web3Modal, ethereumClient, client } from '../web3';

	import { prepareWriteContract, writeContract } from '@wagmi/core';

	async function wrapETH() {
		const config = await prepareWriteContract({
			address: '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6',
			abi: abi,
			functionName: 'deposit',
			args: [],
			overrides: {
				value: ethers.utils.parseEther('0.01')
			}
		});
		const data = await writeContract(config);
		console.log('wrapETH');
	}
</script>

<svelte:head>
	<title>Wrap ETH</title>
	<meta name="description" content="Dice Roll" />
</svelte:head>

<section>
	<button on:click={wrapETH}>Wrap ETH</button>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		/* flex: 0.6; */
	}
</style>
