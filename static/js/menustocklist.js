let socket = io.connect(window.location.origin	);
let hotlist = document.getElementById("hotul");


let gainers = [];
let losers = [];
let total = [];

socket.on("message", function(data){
	if(data["type"] === "hotstocks"){
		//<li class="hotstock"><a href="">OwO</a></li>
		hotlist.innerHTML = "";
		let container;
		let link;
		let price_data;
		for(s of Object.keys(data["data"])){
			//console.log(s)
			let color;
			if(data["data"][s]["change"][0] == "+"){
				color = "rgb(105, 226, 56)";
				gainers.push(s)
			}
			else{
				color = "rgb(255, 46, 25)";
				losers.push(s)
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
			hotlist.appendChild(container);
			
		}
	}
});

socket.send('hotstocks');

