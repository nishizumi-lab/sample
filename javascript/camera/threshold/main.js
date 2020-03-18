// カラー画像を2値画像に変換
function colorToThreshold(color, gray, th) {
  for (var i = 0; i < color.length; i += 4) {
    g = 0.299*color[i+0] + 0.587*color[i+1] + 0.114*color[i+2];  //グレースケール値を計算
	// 閾値で2値化
	if( g > th) gray[i/4] = 255;
	else  gray[i/4] = 0;
  }
}

// グレースケール画像を描画
function drawGrayImg(gray, ctx, imgData){
  var n = gray.length*4;
  var color = new Uint8ClampedArray(n);
  // グレースケールからカラーに変換
  for (var i = 0; i < n; i += 4){
    color[i+0] = gray[i/4];
    color[i+1] = gray[i/4];
    color[i+2] = gray[i/4];
    color[i+3] = 255;
  }
  imgData.data.set(color); 							// imgDataに結果を設定する
  ctx.putImageData(imgData, 0, 0); 				// 画像の描画
}

// カメラ映像の描画
function showVideo(){
  // 変数の定義
  var cvs = document.getElementById("cv");
  var ctx = cvs.getContext("2d");
  var btn = document.getElementById("btn");　		//ボタンハンドラ
  var video = document.getElementById("video");  //ビデオハンドラ
  var w = cvs.width;                                   // canvusの幅
  var h = cvs.height;                                  // canvusの高さ
  var gray = new Uint8ClampedArray(w*h); 	// tの画像
  var btnflag = true;   								// ボタンの判定

  // Videoタグ
  navigator.getMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
  navigator.getMedia ({ video:true, audio:true }, function(stream) { video.src = window.URL.createObjectURL(stream); }, function(err){console.log(err);});

  //ボタンイベント処理
  btn.onclick = function(){
    if (btnflag) {
      video.play(); 									// ビデオ再生
      requestAnimationFrame(onFrame); 	// 動体検出開始
      btnflag = false;
    }
  };

  // 繰り返し行う処理    
  var onFrame = function () {   
    ctx.drawImage(video, 0, 0, w, h); 						// 画像の取得
    var imgData = ctx.getImageData(0, 0, w, h);
    colorToThreshold(imgData.data, gray, 122); 		// 画像を2値化
    requestAnimationFrame(onFrame); 					// 再帰
    drawGrayImg(gray, ctx, imgData); 					// 2値化画像を描画
	
  };
}
