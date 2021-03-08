let socket = io.connect(window.location.origin	);
let symbol = document.getElementById("stockname").innerText;
let comp_name = document.getElementById("companyname");
let price = document.getElementById("price");
let hotlist = document.getElementById("hotul");
let old_price = 0;
let new_price = 0;

socket.on("message", function(data){
	if(data["type"] === "history"){
		chart.data["labels"] = Object.keys(data["data"]).reverse();
		chart.data["datasets"][0]["data"] = Object.values(data["data"]).reverse();
		chart.update();
	}
	else if(data["type"] === "name"){
		comp_name.innerText = data["data"];
	}
	else if(data["type"] === "update"){
		new_price = data["data"]
		//console.log(new_price)
		if(new_price != old_price){
			ChangeValue(getDate(), new_price, chart);
			price.innerText = "$" + parseFloat(new_price);
			document.title = symbol + " STONKS! - $" + new_price;
			old_price = new_price;
		}	
	}
	else if(data["type"] === "hotstocks"){
		//<li class="hotstock"><a href="">OwO</a></li>
		hotlist.innerHTML = "";
		for(s of Object.keys(data["data"])){
			//console.log(s)
			let color;
			if(data["data"][s]["change"][0] == "+"){
				color = "rgb(105, 226, 56)";
			}
			else{
				color = "rgb(255, 46, 25)";
			}
			hotlist.innerHTML += "<li class='hotstock'><a href='/stocks/"+s+"'>" + data["data"][s]["company"] +" - <span style='color:"+color+"'>$" + data["data"][s]["price"]  +"</span></a></li>\n";
		}
	}
	else{
		window.location.location =  window.location.origin 
	}
});




function update_time_values(time){
	socket.send("history "+symbol+" "+ time);
}


update_time_values(7);
socket.send("name "+ symbol);
socket.send("hotstocks");
setInterval(function(){
	socket.send("hotstocks");
}, 120000);


setInterval(function(){
	socket.send("update " + symbol);
}, 3000);


let today = document.getElementById("today");
let week = document.getElementById("week");
let month = document.getElementById('month');
let year = document.getElementById("year");

today.addEventListener("click", function(){
	chart.data["labels"] = []
    chart.data["datasets"][0]["data"] = []
    chart.update()
});


week.addEventListener("click", function(){update_time_values(7)});
month.addEventListener("click", function(){update_time_values(31)});
year.addEventListener("click", function(){update_time_values(365)});