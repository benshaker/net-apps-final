function hist_listener() {
	var myobj = JSON.parse(this.responseText);
	var coll = ["Time of Occurrence", "Animal Detected", "Alarm Sounded", "Lights Flashed", "Image Captured"];
	var col = ['time_of_occurrence', 'animal_detected', 'action_sound', 'action_light', 'image'];
	console.log(myobj);
	for (var key in myobj[0]) {
		if (col.indexOf(key) === -1) {
			col.push(key);
		}
	}
	
	var table = document.createElement("table");
	table.cellSpacing = 25;
	
	var tr = table.insertRow(-1);
	
	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");
		th.innerHTML = coll[i];
		tr.appendChild(th);
	}

	// loading most recent first
	for (var i = myobj.length - 1; i >= 0; i--) {

		tr = table.insertRow(-1);
		for (var j = 0; j < col.length; j++) {

			var tabCell = tr.insertCell(-1);

			if(myobj[i][col[j]] == null){
				myobj[i][col[j]] = "None";
			}
			else if(myobj[i][col[j]] == "default"){
				myobj[i][col[j]] = "Unlisted (default)";
			}
			else if(isBase64(myobj[i][col[j]])){
				var image = new Image();
				image.src = "data:image/png;base64,"+myobj[i][col[j]];

				myobj[i][col[j]] = "<a target=\"_blank\" href=\"#\" onClick=\'view(this)\'><img style=\"width:125px\" alt=\"img_cap\" src="+image.src+"><\a>";
			}
			
			tabCell.innerHTML = myobj[i][col[j]];
			
		}
	}
	var divContainer = document.getElementById("tablePrint");
	divContainer.appendChild(table);
}

function view(element) {
        var newTab = window.open();
        
	tempHTML = element.innerHTML.replace('125px', '500px');
	tempHTML = '<center>' + tempHTML + '</center>';
	newTab.document.body.innerHTML = tempHTML;
        return false;
    }

function isBase64(str) {
    if (str ==='' || str.trim() ==='' || str.length < 100){ return false; }
    try {
        return btoa(atob(str)) == str;
    } catch (err) {
        return false;
    }
}

const Http = new XMLHttpRequest();
Http.addEventListener("load", hist_listener);
const url='/load_history';
Http.open("GET", url);
Http.send();