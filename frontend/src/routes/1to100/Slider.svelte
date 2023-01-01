<script>
	let value = 50;
	let styles = {
		'lower-color': '#55FF55',
		'higher-color': '#FF5555',
		value: value / 100
	};

	let sliderBackground = () => {
		return `linear-gradient(left top,right top,color-stop(0.5, var(--lower-color)),color-stop(0.5, var(--higher-color)));`;
		// return "red";
	};
	console.log("🚀 | sliderBackground | sliderBackground", sliderBackground())
	$: cssVarStyles = Object.entries(styles)
		.map(([key, value]) => `--${key}:${value}`)
		.join(';');
</script>

<div style={cssVarStyles}>
	<div class="game-container">
		<!-- <div class="range">

			<div class="lower above" style="width: {value}%" />
			<div class="higher above" style="width: {100 - value}%" />
		</div> -->
		<input
			min="2"
			max="98"
			class="custom-slider"
			type="range"
			bind:value
			style="background: linear-gradient(to right, #55FF55 {value}%, #FF5555 {value}%)"
		/>
	</div>
</div>
<p>Value: {value}</p>

<style>
	.game-container {
		display: flex;
		align-self: center;
		width: 100%;
		height: 100%;
	}
	
	.custom-slider {
		/* change the appearance of the track and thumb */
		-webkit-appearance: none; /* Override default CSS styles */
		appearance: none;
		width: 100%; /* Full-width */
		background: none; /* Grey background */
		-webkit-transition: 0.2s; /* 0.2 seconds transition on hover */
		transition: opacity 0.2s;
		position: absolute;
		z-index: 10;
	}
	/* The slider handle (use -webkit- (Chrome, Opera, Safari, Edge) and -moz- (Firefox) to override default look) */
	/* style the thumb of the slider */
	.custom-slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 25px;
		height: 25px;
		background: #fff;
		border-radius: 50%;
		cursor: pointer;
	}

	.custom-slider::-webkit-slider-runnable-track {
		/* background-image: -webkit-gradient(
        linear,
        left top,
        right top,
        color-stop(0.5, var(--lower-color)),
        color-stop(0.5, var(--higher-color))
        ); */
		height: 8px; /*trackHeight*/
		border-radius: 4px; /*trackHeight*/
		transition: 0.3s;
	}
	.range {
		position: relative;
		pointer-events: none;
		overflow: hidden;
		width: 100%;
	}

	.lower {
		/* change the appearance of the track and thumb */
		height: 5px;
		width: 100%;
		border-radius: 100px;
		position: absolute;
		left: 0;
	}

	.lower.above {
		/* change the appearance of the track and thumb */
		background: var(--lower-color);
	}

	.higher {
		/* change the appearance of the track and thumb */
		height: 5px;
		width: 100%;
		border-radius: 100px;
		position: absolute;
		right: 0;
	}

	.higher.above {
		/* change the appearance of the track and thumb */
		background: var(--higher-color);
	}
</style>
