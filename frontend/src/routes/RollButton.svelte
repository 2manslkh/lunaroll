<script>
	import Dice from './Dice.svelte';

    let roll = 0;
  
    function rollDice() {
      roll = Math.floor(Math.random() * 6) + 1;
    }
</script>

<style>
    button {
      width: 100%;
      padding: 10px 20px;
      border-radius: 5px;
      background-color: #69E444;
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
  
<div>
    <Dice value={roll}/>
    <button on:click={rollDice}>Roll Dice</button>
</div>


  
