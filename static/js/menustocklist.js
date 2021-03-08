let socket = io.connect(window.location.origin	);
let hotlist = document.getElementById("hotul");


socket.on("message", function(data){
	if(data["type"] === "hotstocks"){
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
			hotlist.innerHTML += "<li class='hotstock'><a href='/stocks/"+s+"'>" + data["data"][s]["company"] +" - <span style='color:"+color+"'>$" + data["data"][s]["price"]  +"</span></a></li>\n"
		}
	}
});

socket.send('hotstocks');

