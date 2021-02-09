

let mychart = document.getElementById("chart").getContext("2d");
let name = document.getElementById('stockname').innerText;
Chart.defaults.global.defaultFontColor = 'white';
let chart = new Chart(mychart, {
	type: "line",
	data: {
		labels: [1,2,3,4,5,6,7,8],
		datasets:[
			{
				data:[10,11,12,13,14,15,16,200],
				label: name,
				borderColor: "#ffff00",

			}
		]

	}
});



function ChangeValue(){}