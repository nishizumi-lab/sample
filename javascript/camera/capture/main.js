// カメラのキャプチャー
function capCamera(){
  navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || window.navigator.mozGetUserMedia;
    window.URL = window.URL || window.webkitURL;
 
  var video = document.getElementById("camera");
  var localStream = null;
  navigator.getUserMedia({video: true, audio: false},
  // カメラのキャプチャーに成功した場合
  function(stream) {
    console.log(stream);
    video.src = window.URL.createObjectURL(stream);
  },
  // カメラのキャプチャーに失敗した場合
  function(err) {
    console.log(err);
  }
  );
}
