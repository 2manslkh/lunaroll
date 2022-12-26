<script>
	import Dice from './Dice.svelte';

    let roll = 0;
  
    function rollDice() {
      roll = Math.floor(Math.random() * 6) + 1;
    }
</script>

<style>
    button {
      font-size: 18px;
      padding: 10px 20px;
      border-radius: 5px;
      background-color: #69E444;
      border: none;
    }
    p {
      font-size: 24px;
      font-weight: bold;
    }
</style>
  
<Dice value={roll}/>

<button on:click={rollDice}>Roll Dice</button>

  
