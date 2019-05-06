(function() {
  window.onload=function(){
    const save_btn = document.getElementById("save");
    if(save_btn){
      save_btn.addEventListener("click", RespondClick);
    }
  }

  function reqListener () {
    res_arr   = JSON.parse(this.responseText);
    //console.log(res_arr);
    for (var i = 3; i >= 0; i--) {
      name = res_arr[i]["name"];
      //console.log(res_arr[i]);
      if(name.includes('time')){
	//console.log('true');
        val = JSON.stringify(res_arr[i][name]);
      }
      else val = res_arr[i][name];
      //console.log(name);
      //console.log(val);

      document.getElementById(name).value = val;
    };
  }

  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "/load_settings");
  xhr.send();

  function RespondClick() {
      whitelist = document.getElementById("whitelist").value.split(",");
      whitelist = {"whitelist":whitelist, "name":"whitelist"}
      // console.log(whitelist)
      blacklist = document.getElementById("blacklist").value.split(",");
      blacklist = {"blacklist":blacklist, "name":"blacklist"}
      // console.log(blacklist)
      daytime   = document.getElementById("daytime").value.split(",");
      daytime = {"daytime":JSON.parse(daytime), "name":"daytime"}
      // console.log(daytime)
      nighttime = document.getElementById("nighttime").value.split(",");
      nighttime = {"nighttime":JSON.parse(nighttime), "name":"nighttime"}
      // console.log(nighttime)

      data = {'data': [whitelist, blacklist, daytime, nighttime]}

      var xhr = new XMLHttpRequest();
      xhr.open("PUT", "/save_settings");
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify(data));
  }
})();