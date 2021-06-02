
let update_handler = io.connect(window.location.origin);
let symbols = document.getElementsByClassName("stocksymbol");
let prices = document.getElementsByClassName("bghtp");
let quantities = document.getElementsByClassName("qty");
let earnings = document.getElementsByClassName("earnedd");
let current_value = document.getElementsByClassName("teller moneytell")[1];
let total_earned = document.getElementsByClassName("totalearned")[0];

let current_stock_values = {};

setInterval(function(){
	let symbol;
	let price;
	let quantity;
	let total;
	let last_earned;
	let checksum_total_earched = 0;
	let current_value_update = 0;
	for(let i=0; i < symbols.length; i++){
		symbol = symbols[i].innerText
		quantity = parseInt(quantities[i].innerText);
		price = parseFloat(prices[i].innerText);
		earning = earnings[i];
		last_earned = earning.innerText;
		//console.log('--------------- updating ' + symbol + " owo");
		update_handler.send("update " + symbol);
		total = (current_stock_values[symbol] * quantity) - (price * quantity)
		checksum_total_earched += total;
		current_value_update += current_stock_values[symbol] * quantity;
		if(isNaN(total)){
			continue;
		}
		if(total > 0){
			earning.style.color = "rgb(105, 226, 51)";
			earning.innerText = "+" + total.toFixed(2);
		}
		else if(total < 0){
			earning.style.color = "rgb(255, 46, 25)";
			earning.innerText = earning.innerText = total.toFixed(2);
		}
		else{
			if(last_earned != total.toFixed(2)){
				earning.style.color = "white";
				earning.innerText = earning.innerText = total.toFixed(2);
			}				
		}
	}
	if(!isNaN(current_value)){
			current_value.innerText = "$" + current_value_update.toFixed(2);;
	}
	if(!isNaN(checksum_total_earched)){
		if(checksum_total_earched > 0){
			total_earned.style.color = "rgb(105, 226, 51)";
			total_earned.innerText = "+" + checksum_total_earched.toFixed(2);
		}
		else if(checksum_total_earched < 0){
			total_earned.style.color = "color:rgb(255, 46, 25)";
			total_earned.innerText = checksum_total_earched.toFixed(2);
		}
		else{
			total_earned.style.color = "white";
			total_earned.innerText = "0.0";
		}
	}



}, 1500);



update_handler.on("message", function(data){
	//console.log(data);
	if(data['type'] === 'update'){
		current_stock_values[data['symbol']] = parseFloat(data['data']);
		//console.log(data['data']);
	}
});