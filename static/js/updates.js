let socket = io.connect("http://127.0.0.1:5000");

console.log(chart)

socket.on("message", function(data){
	if(data["type"] == "history"){
		for(date of Object.keys(data["data"]).reverse()){
			console.log(date)
			console.log(data["data"][date])
			console.log(data)
			ChangeValue(date, data["data"][date], chart)
		}
	}
});

socket.send("history GME")