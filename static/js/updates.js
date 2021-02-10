let socket = io.connect("http://127.0.0.1:5000");
let symbol = document.getElementById("stockname").innerText;
let comp_name = document.getElementById("companyname");
let price = document.getElementById("price");

socket.on("message", function(data){
	console.log(data)
	if(data["type"] === "history"){
		chart.data["labels"] = Object.keys(data["data"]).reverse();
		chart.data["datasets"][0]["data"] = Object.values(data["data"]).reverse();
		chart.update();
	}
	else if(data["type"] === "name"){
		console.log(data["data"]);
		comp_name.innerText = data["data"];
	}
	else if(data["type"] === "update"){
		ChangeValue(data["data"][0], parseFloat(data["data"][1]), chart);
		price.innerText = "$" + parseFloat(data["data"][1]);
	}
});




function update_time_values(time){
	socket.send("history "+symbol+" "+ time);
}


update_time_values(7);
socket.send("name "+ symbol);


let week = document.getElementById("week");
let month = document.getElementById('month');
let year = document.getElementById("year");

week.addEventListener("click", function(){update_time_values(7)});
month.addEventListener("click", function(){update_time_values(31)});
year.addEventListener("click", function(){update_time_values(365)});