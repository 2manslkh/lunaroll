<script lang="ts">
	export let value = 1;
	import dice_1 from '$lib/images/dice/Dice 1.svg';
	import dice_2 from '$lib/images/dice/Dice 2.svg';
	import dice_3 from '$lib/images/dice/Dice 3.svg';
	import dice_4 from '$lib/images/dice/Dice 4.svg';
	import dice_5 from '$lib/images/dice/Dice 5.svg';
	import dice_6 from '$lib/images/dice/Dice 6.svg';

	const dice_map = {
		1: dice_1,
		2: dice_2,
		3: dice_3,
		4: dice_4,
		5: dice_5,
		6: dice_6
	};
</script>

<!-- add padding -->

<div class="die" style="padding: 10px;">
	{#if value === 1}
		<img src={dice_1} alt="Dice {value}" />
	{:else if value === 2}
		<img src={dice_2} alt="Dice {value}" />
	{:else if value === 3}
		<img src={dice_3} alt="Dice {value}" />
	{:else if value === 4}
		<img src={dice_4} alt="Dice {value}" />
	{:else if value === 5}
		<img src={dice_5} alt="Dice {value}" />
	{:else if value === 6}
		<img src={dice_6} alt="Dice {value}" />
	{:else}
		<img src={dice_1} alt="Dice {value}" />
	{/if}
</div>

<style>
	/* style the component as needed */
	.die {
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
