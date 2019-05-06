(function() {
  window.onload=function(){
    const save_btn = document.getElementById("save");
    if(save_btn){
      save_btn.addEventListener("click", RespondClick);
    }
  }

  function reqListener () {
    res_arr   = JSON.parse(this.responseText);
    for (var i = res_arr.length - 1; i >= 0; i--) {
      name = res_arr[i]["name"];

      if(name.includes('time')){
        val = JSON.stringify(res_arr[i][name]);
      }
      else val = res_arr[i][name];

      document.getElementById(name).value = val;
    };
    // console.log(res_arr[0]["whitelist"])
    // console.log(res_arr[1]["blacklist"])
    // console.log(res_arr[2]["daytime"])
    // console.log(res_arr[3]["nighttime"])
    // whitelist = res_arr[0]["whitelist"];
    // blacklist = res_arr[1]["blacklist"];
    // daytime   = JSON.stringify(res_arr[2]["daytime"]);
    // nighttime = JSON.stringify(res_arr[3]["nighttime"]);

    // document.getElementById("white").value = whitelist;
    // document.getElementById("black").value = blacklist;
    // document.getElementById("day").value = daytime;
    // document.getElementById("night").value = nighttime;
  }

  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "http://localhost:8080/load_settings");
  xhr.send();

  function RespondClick() {
      whitelist = document.getElementById("white").value.split(",");
      whitelist = {"whitelist":whitelist, "name":"whitelist"}
      // console.log(whitelist)
      blacklist = document.getElementById("black").value.split(",");
      blacklist = {"blacklist":blacklist, "name":"blacklist"}
      // console.log(blacklist)
      daytime   = document.getElementById("day").value.split(",");
      daytime = {"daytime":JSON.parse(daytime), "name":"daytime"}
      // console.log(daytime)
      nighttime = document.getElementById("night").value.split(",");
      nighttime = {"nighttime":JSON.parse(nighttime), "name":"nighttime"}
      // console.log(nighttime)

      data = {'data': [whitelist, blacklist, daytime, nighttime]}

      var xhr = new XMLHttpRequest();
      xhr.open("PUT", "http://localhost:8080/save_settings");
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify(data));
  }
})();