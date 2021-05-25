let searcher = io.connect(window.location.origin);
let go = document.getElementById("go");
let searchbar = document.getElementById("search");
let results = document.getElementById("searchresult");
let ulresults = document.getElementById("sresults");
results.style.display = 'none';

let navigations = document.getElementsByClassName("navli");

for(navli of navigations){
	navli.addEventListener('click', function(){
		let uri = this.innerText.toLowerCase();
		window.location = "/" + uri; 
	});
}

document.addEventListener("click", function(e){
	let id = e.target.id;

	if(id != 'searchresult' && id != 'search'){
		results.style.display = 'none';
	}
	else{
		let rs = document.getElementsByClassName("srchresult");
		if(rs.length > 0){
			results.style.display = 'block';
		}
		
	}
});
let SYMBOLS = {};
searcher.on("message", function(data){
	if(data["type"] === 'symbols'){
		SYMBOLS = data['data'];
		//console.log(SYMBOLS);
		searcher.disconnect();
	}
});

searcher.send('symbols'); 


function search(string){
	let resultsl = [];
	if(string === ''){
		results.style.display = "none";
		return ''
	}
	for(let company of Object.keys(SYMBOLS)){
		if(company.toLowerCase().indexOf(string.toLowerCase()) != -1 || SYMBOLS[company].toLowerCase().indexOf(string.toLowerCase()) != -1){
			content = '<li class="srchresult" value="'+ SYMBOLS[company] +'">'+ company +'</li>';
			resultsl.push(content);
		}
	}
	if(resultsl.length > 0){
		results.style.display = "block";
	}
	else{
		results.style.display = "none";
	}
	resultsl = resultsl.join("\n");
	return resultsl;;
}

searchbar.addEventListener("input", function(){
	let resultss = search(searchbar.value);
	console.log(resultss);
	ulresults.innerHTML = resultss;
});

searchbar.onkeypress = function(e){
	if (!e) e = window.event;
    var keyCode = e.code || e.key;
    if (keyCode == 'Enter'){
      let options = document.getElementsByClassName("srchresult");
      if(options.length > 0){
      	options[0].click();
      }
      else{
      	go.click();
      }
      return false;
    }
}


window.addEventListener("click", function(e){
	if(e.target.className == 'srchresult'){
		window.location.href = window.location.origin + "/stocks/" + e.target.getAttribute('value');
	}
});


go.addEventListener("click", function(){
	window.location.href = window.location.origin + "/stocks/" + searchbar.value;
});