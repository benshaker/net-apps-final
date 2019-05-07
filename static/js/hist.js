function hist_listener() {
	var myobj = JSON.parse(this.responseText);
	var coll = ["Time of Occurrence", "Image Captured", "Animal Detected", "Best Guesses", "Alarm Sounded", "Lights Flashed"];
	var col = ['time_of_occurrence', 'image', 'animal_detected', 'labels', 'action_sound', 'action_light'];
	for (var key in myobj[0]) {
		if (col.indexOf(key) === -1) {
			col.push(key);
		}
	}
	
	var table = document.createElement("table");
	table.cellSpacing = 25;
	table.style.borderCollapse = "collapse";
	table.width = "100%";
	
	var tr = table.insertRow(-1);
	
	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");
		th.style.textAlign = 'center';
		th.style.padding = "25px";
		th.innerHTML = coll[i];
		tr.appendChild(th);
	}

	// loading most recent first
	for (var i = myobj.length - 1; i >= 0; i--) {

		tr = table.insertRow(-1);
		for (var j = 0; j < col.length; j++) {

			var tabCell = tr.insertCell(-1);
			tabCell.style.textAlign = 'center';

			if(myobj[i][col[j]] == null){
				myobj[i][col[j]] = "None";
			}
			else if(col[j] == "labels"){
				myobj[i][col[j]] = "<button class=\"btn btn--sm btn--outline\" style=\"white-space: normal;\" onclick=\'myFunction(this)\'><span style=\"display:block;\">Show/Hide</span><span style=\"font-size:10px;display:none;\"><br/>"+myobj[i][col[j]]+"</span></button>";
			}
			else if(myobj[i][col[j]] == "default"){
				myobj[i][col[j]] = "Unlisted (default)";
			}
			else if(isBase64(myobj[i][col[j]])){
				var image = new Image();
				image.src = "data:image/png;base64,"+myobj[i][col[j]];

				myobj[i][col[j]] = "<a target=\"_blank\" href=\"#\" onClick=\'view(this)\'><img style=\"width:350px\" alt=\"img_cap\" src="+image.src+"><\a>";
			}
				
			tabCell.style.padding = "25px";
			tabCell.innerHTML = myobj[i][col[j]];
		}
		tr.style.borderBottom = "1px solid lightgray";
		tr.style.height = "175px";
	}
	var divContainer = document.getElementById("tablePrint");
	divContainer.appendChild(table);
}

function view(element) {
        var newTab = window.open();
        
	tempHTML = element.innerHTML.replace('350px', '700px');
	tempHTML = '<center>' + tempHTML + '</center>';
	newTab.document.body.innerHTML = tempHTML;
        return false;
    }

function isBase64(str) {
    if (typeof str === 'string' || str instanceof String) {}
    else return false;
    if (str ==='' || str.trim() ==='' || str.length < 100){ return false; }
    try {
        return btoa(atob(str)) == str;
    } catch (err) {
        return false;
    }
}

function myFunction(element) {
  og = element.innerHTML;
  og = element.innerHTML.replace(/,/g, ', ');
  let replaced = og.replace(/(?:none|block)/g, o => {
  	return o === "none" ? "block" : "none";
  });
  element.innerHTML = replaced;
}

const Http = new XMLHttpRequest();
Http.addEventListener("load", hist_listener);
const url='/load_history';
Http.open("GET", url);
Http.send();