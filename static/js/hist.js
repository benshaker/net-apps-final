function hist_listener() {
	var myobj = JSON.parse(this.responseText);
	var coll = ["Time of occurrence    ", "Animal detected   ", "Sound used    ", "Light used    "];
	var col = ['time_of_occurrence', 'animal_detected', 'action_sound', 'action_light'];
	console.log(myobj[0]);
	for (var key in myobj[0]) {
		if (col.indexOf(key) === -1) {
			col.push(key);
		}
	}
	
	var table = document.createElement("table");
	
	var tr = table.insertRow(-1);
	
	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");
		th.innerHTML = coll[i];
		tr.appendChild(th);
	}

	# loading most recent first
	for (var i = myobj.length - 1; i >= 0; i--) {
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
const url='/load_history';
Http.open("GET", url);
Http.send();