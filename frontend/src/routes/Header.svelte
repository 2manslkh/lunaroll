<script>
	import { page } from '$app/stores';
	import logo from '$lib/images/LUNAR_ROLL_header.svg';
	import github from '$lib/images/github.svg';
</script>

<header>
	<div class="header-logo">
		<img src={logo} alt="LunarRoll"/>
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
		width: 100%;
	}
	.header-logo img {
   		/* padding: 10px; */
		width: 100%;
	}

</style>
