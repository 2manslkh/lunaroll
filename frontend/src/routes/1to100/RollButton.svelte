<script>
	import Dice from './Dice.svelte';

	let value = 0;
	let isRolling = false;

	function rollDice() {
		value = Math.floor(Math.random() * 6) + 1;
	}
</script>

<div>
	<Dice {value} />
	<button on:click={rollDice}>Roll Dice</button>
</div>

<style>
	button {
		width: 100%;
		padding: 10px 20px;
		border-radius: 5px;
		background-color: #69e444;
		border: none;
		font-size: 24px;
		font-weight: bold;
		font-family: 'Raleway';
		font-style: normal;
		font-weight: 700;
		font-size: 14px;
		line-height: 16px;
	}

	p {
		font-size: 24px;
		font-weight: bold;
		font-family: Raleway;
		font-style: normal;
		font-weight: 700;
		font-size: 14px;
		line-height: 16px;
	}
</style>
