
function report() {
  const params = new URLSearchParams(location.search);
  const domain = params.get("domain");
  if (domain == null) {
    document.getElementById("result").innerHTML = '你还没有进行检查哦~';
  }
  else{
  var xmlhttp = new XMLHttpRequest();
  var url = "https://api.ninym.top/hexo-link-check/report?domain=" + domain;
  var type = "GET"; //方法
  xmlhttp.open(type, url, true); //方法，接口，异步
  xmlhttp.send(); //发送请求
  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.status == 200 && xmlhttp.readyState == 4) {
      document.getElementById("result").innerHTML = xmlhttp.responseText;
    }
  };
}
}

function open() {
  window.open("https://api.ninym.top/hexo-link-check/report?domain=" + document.getElementById('domain').value);'));
}