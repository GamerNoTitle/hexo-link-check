function report(){
  $.ajax({
      url: "https://api.ninym.top/hexo-link-check/report",
      type: "get",
      dataType: "text",
      success: function(data){
          /*这个方法里是ajax发送请求成功之后执行的代码*/
          showData(data.data);//我们仅做数据展示
      },
      error: function(msg){
          alert("ajax连接异常："+msg);
      }
  });
  showData(data)
};
//展示数据
function showData(data) {
    var str = "";//定义用于拼接的字符串
    document.getElementById("status").innerHTML=data.data; 
    }