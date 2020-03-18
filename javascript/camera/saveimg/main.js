// カメラのキャプチャー
function capCamera(){
  navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || window.navigator.mozGetUserMedia;
    window.URL = window.URL || window.webkitURL;
  
  var video = document.getElementById("dispVideo");
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

// キャンバスにコピー
function video2Cvs() {
  // キャンバスの作成
  var cvs = document.getElementById("cv");
  var ctx = cvs.getContext("2d");
  // Videoの取得
  var vle = document.getElementById("dispVideo");
  // canvasの幅と高さを動画の幅と高さに設定
  cvs.width  = vle.videoWidth;   
  cvs.height = vle.videoHeight;
  // canvasに動画のフレームを描画
  ctx.drawImage(vle, 0, 0);  
}
