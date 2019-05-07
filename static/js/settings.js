$(document).ready(function() {
  window.onload=function(){
    const save_btn = document.getElementById("save");
    if(save_btn){
      save_btn.addEventListener("click", RespondClick);
    }
  }

  function reqListener () {
    res_arr   = JSON.parse(this.responseText);
    for (var i = 3; i >= 0; i--) {
      name = res_arr[i]["name"];
      if(name.includes('time')){
        val = JSON.stringify(res_arr[i][name]);
      }
      else val = res_arr[i][name];

      document.getElementById(name).value = val;
    };
  }


  var xhr = new XMLHttpRequest();
  var xhr1 = new XMLHttpRequest();
  xhr1.addEventListener("load", reqListener);
  xhr1.open("GET", "/load_settings");
  xhr1.send();

  function RespondClick() {

      whitelist_list = document.getElementById("whitelist").value.split(",");
      whitelist = {"whitelist":whitelist_list, "name":"whitelist"}
      blacklist_list = document.getElementById("blacklist").value.split(",");
      blacklist = {"blacklist":blacklist_list, "name":"blacklist"}
      daytime   = document.getElementById("daytime").value.split(",");
      daytime_json = JSON.parse(daytime);
      daytime = {"daytime":daytime_json, "name":"daytime"}
      nighttime = document.getElementById("nighttime").value.split(",");
      nighttime_json = JSON.parse(nighttime);
      nighttime = {"nighttime":nighttime_json, "name":"nighttime"}

      for(var i = blacklist_list.length - 1; i >= 0; i --){
	if (!(blacklist_list[i] in nighttime_json)){
	  $("#error-alert").text("\u274c Missing Nighttime Response for \""+blacklist_list[i]+"\".");
	  $("#error-alert").show();
	  setTimeout(function() {
		$("#error-alert").hide();
		$("#error-alert").text("\u10060 Save Not Successful");
		}, 4000)
	  return false;
	} else if (!(blacklist_list[i] in daytime_json)){
	  $("#error-alert").text("\u274c Missing Daytime Response for \""+blacklist_list[i]+"\".");
	  $("#error-alert").show();
	  setTimeout(function() {
		$("#error-alert").hide();
		$("#error-alert").text("\u10060 Save Not Successful");
		}, 4000)
	  return false;
	}
      }

      data = {'data': [whitelist, blacklist, daytime, nighttime]}

      
      xhr.open("PUT", "/save_settings");
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify(data));
  }

  xhr.onreadystatechange = function() {
       if (xhr.readyState === 4) {
        var response = JSON.parse(xhr.responseText);
        if (xhr.status === 200 && response.status === 'OK') {
           $("#success-alert").show();
	   setTimeout(function() { $("#success-alert").hide(); }, 2000);
        } else {s
           $("#error-alert").show();
	   setTimeout(function() { $("#error-alert").hide(); }, 2000);
        }
       }
      }
});