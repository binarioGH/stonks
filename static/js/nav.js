let searcher = io.connect(window.location.origin);
let searchbar = document.getElementById("search");
let results = document.getElementById("searchresult");
let ulresults = document.getElementById("sresults");
results.style.display = 'none';

let navigations = document.getElementsByClassName("navli");

for(navli of navigations){
	navli.addEventListener('click', function(){
		let uri = this.innerText.toLowerCase();
		window.location = uri;
	});
}

document.addEventListener("click", function(e){
	let id = e.target.id;

	if(id != 'searchresult' && id != 'search'){
		results.style.display = 'none';
	}
	else{
		results.style.display = 'block';
	}
});
let SYMBOLS = {};
searcher.on("message", function(data){
	if(data["type"] === 'symbols'){
		SYMBOLS = data['data'];
		console.log(SYMBOLS);
		searcher.disconnect();
	}
});

searcher.send('symbols'); 


function search(string){
	let results = [];
	for(let company of Object.keys(SYMBOLS)){
		if(company.toLowerCase().indexOf(string.toLowerCase()) != -1 || SYMBOLS[company].toLowerCase().indexOf(string.toLowerCase()) != -1){
			content = '<li class="srchresult" value="'+ SYMBOLS[company] +'">'+ company +'</li>';
			results.push(content);
		}
	}
	results = results.join("\n");
	return results;
}

searchbar.addEventListener("input", function(){
	let results = search(searchbar.value);
	ulresults.innerHTML = results;
});


window.addEventListener("click", function(e){
	if(e.target.className == 'srchresult'){
		window.location.href = window.location.origin + "/stocks/" + e.target.getAttribute('value');
	}
});