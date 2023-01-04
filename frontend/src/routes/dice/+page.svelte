<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import RollButton from './RollButton.svelte';
</script>

<svelte:head>
	<title>Dice Roll</title>
	<meta name="description" content="Dice Roll" />
</svelte:head>

<section>
	<RollButton />
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
