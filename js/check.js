function submit() {
  var params = {
    domain: document.getElementsByName("domain").value,
    linkpath: document.getElementsByName("linkpath").value,
  };
  httpPost("http://api.ninym.top/check", params);
}

function httpPost(URL, PARAMS) {
  var temp = document.createElement("form");
  temp.action = URL;
  temp.method = "post";
  temp.style.display = "none";

  for (var x in PARAMS) {
    var opt = document.createElement("textarea");
    opt.name = x;
    opt.value = PARAMS[x];
    temp.appendChild(opt);
  }

  document.body.appendChild(temp);
  temp.submit();

  return temp;
}

function check() {
  var btn = document.getElementById('btn');
  var domain = document.getElementById('domain');
  var path = document.getElementById('path');
  btn.onclick = function() {
      var xhr = new XMLHttpRequest(); // 1
      var domain = domain.value; // 3
      var path = path.value; // 3
      var params = 'domain=' + domain + '&path=' + path; // 3
      xhr.open('post', 'ttp://api.ninym.top/hexo-link-check/check'); // 1
      // 设置请求报文的报文头信息
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

      xhr.send(params); // 注意这里要填请求参数
      // 获取服务器端响应的数据
      xhr.onload = function() {
              console.log(xhr.responseText)
          } // 1
  }
}