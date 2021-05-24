let socket = io.connect(window.location.origin	);
let hotlist = document.getElementById("hotul");

let gainers_button = document.getElementById("gainers");
let losers_button = document.getElementById("losers");

let gainers = [];
let losers = [];
let total = [];
let mode = 'gainers'
socket.on("message", function(data){
	if(data["type"] === "hotstocks"){
		//<li class="hotstock"><a href="">OwO</a></li>
		hotlist.innerHTML = "";
		let container;
		let link;
		let price_data;
		let this_mode;
		for(s of Object.keys(data["data"])){
			//console.log(s)
			let color;
			if(data["data"][s]["change"][0] == "+"){
				color = "rgb(105, 226, 56)";
				this_mode = 'gainer';
			}
			else{
				color = "rgb(255, 46, 25)";
				this_mode = 'loser';
			}
			//Inserting the element sanitized against xss.
			container = document.createElement("li");
			container.classList.add("hotstock");
			link = document.createElement("a");
			link.style.dipslay = 'inline-block';
			link.href = "/stocks/"+s;
			link.innerText = data["data"][s]["company"] + " - "; 
			price_data = document.createElement("span")
			price_data.style.color = color; 
			price_data.style.dipslay = 'inline-block';
			price_data.innerText =  "$" +  data["data"][s]["price"];
			container.appendChild(link);
			link.appendChild(price_data)
			if(this_mode == 'gainer'){
				gainers.push(container); 
			}
			else if(this_mode == 'loser'){
				losers.push(container);
			}
			//hotlist.appendChild(container);
			
		}
		populate(); 
	}
});

socket.send('hotstocks');

function populate(){
	let list;
	gainers_button.style.color = 'white';
	losers_button.style.color = 'white';
	if(mode == 'gainers'){
		list = gainers;
		gainers_button.style.color = '#69e233';
	}
	else if(mode == 'losers'){
		list = losers;
		losers_button.style.color = '#ff2e19';
	}
	hotlist.innerHTML = "";
	for(stock_obj of list){
		hotlist.appendChild(stock_obj);
	}
	console.log(list);
}




gainers_button.addEventListener("click", function(){
	mode = 'gainers';
	populate();
});

losers_button.addEventListener("click", function(){
	mode = 'losers';
	populate();
});