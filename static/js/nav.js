
let searchbar = document.getElementById("search");
let results = document.getElementById("searchresult");
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