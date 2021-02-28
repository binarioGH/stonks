

let navigations = document.getElementsByClassName("navli");


for(navli of navigations){
	navli.addEventListener('click', function(){
		let uri = this.innerText.toLowerCase();
		window.location = uri;
	});
}