<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
</script>

<svelte:head>
	<title>Dice Roll</title>
	<meta name="description" content="Dice Roll" />
</svelte:head>

<section>
	<p>Main Page</p>
	<a href="/dice">Dice</a>
	<a href="/1to100">1 to 100</a>
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
