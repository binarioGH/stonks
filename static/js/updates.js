let socket = io.connect("http://127.0.0.1:5000");
let symbol = document.getElementById("stockname").innerText;
let comp_name = document.getElementById("companyname");
let price = document.getElementById("price");
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
			old_price = new_price;
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
setInterval(function(){
	socket.send("update " + symbol);
}, 3000);

let week = document.getElementById("week");
let month = document.getElementById('month');
let year = document.getElementById("year");

week.addEventListener("click", function(){update_time_values(7)});
month.addEventListener("click", function(){update_time_values(31)});
year.addEventListener("click", function(){update_time_values(365)});