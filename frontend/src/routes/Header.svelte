<script>
	import { page } from '$app/stores';
	import logo from '$lib/images/LUNAR_ROLL_header.svg';
	import github from '$lib/images/github.svg';

	import { web3Modal } from './web3';

	web3Modal.setTheme({themeColor: 'blackWhite'});


</script>

<header>
	<div class="header-logo">
		<img src={logo} alt="LunarRoll" />
		<div class="web3modal-container">
			<w3m-network-switch></w3m-network-switch>
			<w3m-core-button></w3m-core-button>
		</div>
	</div>
</header>

<style>
	.web3modal-container {
		display: flex;
		align-items: top;
		justify-content: center;
	}
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
