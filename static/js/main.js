(function() {
  window.onload=function(){
    const save_btn = document.getElementById("save");
    if(save_btn){
      save_btn.addEventListener("click", RespondClick);
    }
  }

  function reqListener () {
    res_arr   = JSON.parse(this.responseText);
    whitelist = res_arr[0]["whitelist"].toString();
    blacklist = res_arr[1]["blacklist"].toString();
    daytime   = res_arr[2]["response_daytime"].toString();
    nighttime = res_arr[3]["response_nighttime"].toString();

    document.getElementById("white").value = whitelist;
    document.getElementById("black").value = blacklist;
    document.getElementById("day").value = daytime;
    document.getElementById("night").value = nighttime;
  }

  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "http://localhost:8080/load_settings");
  xhr.send();

  function RespondClick() {
      whitelist = document.getElementById("white").value.split(",");
      whitelist = {"whitelist":whitelist, "name":"white"}
      // console.log(whitelist)
      blacklist = document.getElementById("black").value.split(",");
      blacklist = {"blacklist":blacklist, "name":"black"}
      // console.log(blacklist)
      daytime   = document.getElementById("day").value.split(",");
      daytime = {"daytime":daytime, "name":"day"}
      // console.log(daytime)
      nighttime = document.getElementById("night").value.split(",");
      nighttime = {"nighttime":nighttime, "name":"night"}
      // console.log(nighttime)

      data = {'data': [whitelist, blacklist, daytime, nighttime]}

      var xhr = new XMLHttpRequest();
      xhr.open("PUT", "http://localhost:8080/save_settings");
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify(data));
  }
})();