let socket = io.connect(window.location.origin	);
let hotlist = document.getElementById("hotul");


socket.on("message", function(data){
	if(data["type"] === "hotstocks"){
		//<li class="hotstock"><a href="">OwO</a></li>
		hotlist.innerHTML = "";
		for(s of Object.keys(data["data"])){
			console.log(s)
			hotlist.innerHTML += "<li class='hotstock'><a href='/stocks/"+s+"'>"+ data["data"][s]["company"] +" ~ " + data["data"][s]["price"] + " ~ "+ data["data"][s]["change"] +"</a></li>\n"
		}
	}
});

socket.send('hotstocks');
setInterval(function(){
	console.log("sending...");
	socket.send('hotstocks');
}, 3000);
