function hist_listener() {
	var myobj = JSON.parse(this.responseText);
	var coll = ["Animal detected   ", "Time of occurrence    ", "Sound used    ", "Light used    "];
	var col = [];
	for (var i = 0; i < myobj.length; i++) {
		console.log(myobj[i]);
		for (var key in myobj[i]) {
			if (col.indexOf(key) === -1) {
				col.push(key);
			}
		}
	}
	
	var table = document.createElement("table");
	
	var tr = table.insertRow(-1);
	
	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");
		th.innerHTML = coll[i];
		tr.appendChild(th);
	}
	
	for (var i = 0; i < myobj.length; i++) {
		tr = table.insertRow(-1);
		for (var j = 0; j < col.length; j++) {
			var tabCell = tr.insertCell(-1);
			tabCell.innerHTML = myobj[i][col[j]];
		}
	}
	var divContainer = document.getElementById("tablePrint");
	divContainer.appendChild(table);
}

const Http = new XMLHttpRequest();
Http.addEventListener("load", hist_listener);
const url='http://localhost:8080/load_history';
Http.open("GET", url);
Http.send();