// カラー画像をグレースケール画像に変換
function colorToGray(color, gray) {
  for (var i = 0; i < color.length; i += 4) {
    gray[i/4] = 0.299*color[i+0] + 0.587*color[i+1] + 0.114*color[i+2];    // グレースケール値を計算
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
  var cvs = document.getElementById("cv");
  var ctx = cvs.getContext("2d");
  var btn = document.getElementById("btn");　		//ボタンハンドラ
  var video = document.getElementById("video");  //ビデオハンドラ
  var w = video.clientWidth;   						// 映像の幅
  var h = video.clientHeight; 						// 映像の高さ
  var gray = new Array(3);
  gray[0] = new Uint8ClampedArray(w*h); 	// tの画像
  gray[1] = new Uint8ClampedArray(w*h); 	// t+1の画像
  gray[2] = new Uint8ClampedArray(w*h); 	// t+2の画像
  var diff0 = new Uint8ClampedArray(w*h); 	// t  とt+1フレームの差分画像
  var diff1 = new Uint8ClampedArray(w*h); 	// t+1フレームとt+2フレームの差分画像
  var btnflag = true;   								// ボタンの判定
  var count = 0; 										// フレームのカウント 
  // Videoタグ
  navigator.getMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
  navigator.getMedia ({ video:true, audio:true }, function(stream) { video.src = window.URL.createObjectURL(stream); }, function(err){console.log(err);});

  //ボタンイベント処理
  btn.onclick = function(){
    if (btnflag) 
	{
      video.play(); 									// ビデオ再生
      requestAnimationFrame(onFrame); 	// 動体検出開始
      btnflag = false;
    }
  };

  // 繰り返し行う処理    
  var onFrame = function () {   
    var pixcelNum = 0; 										// 動体のピクセル数
    ctx.drawImage(video, 0, 0, w, h); 						// 画像の描画
    var imgData = ctx.getImageData(0, 0, w, h);
    colorToGray(imgData.data, gray[count]); 			// 最新の画像をグレースケール変換
    requestAnimationFrame(onFrame); 					// 再帰
  
    if (count !== 2){  // 画面のクリア
      ctx.clearRect(0, 0, cvs.w, cvs.h);
      count++; return;
    }
    // フレーム間の差分を計算
    for (var i = 0; i < diff0.length; i++){
      diff0[i] = Math.abs(gray[1][i] - gray[0][i]);
      diff1[i] = Math.abs(gray[2][i] - gray[1][i]);
      diff0[i] = (diff0[i] & diff0[i]) * 3; 					// フレーム間差分    
      if(diff0[i] > 150) pixcelNum++; 						// 動体のピクセル数をカウント
    }
    // 動体のピクセル数で検出判定
    if (pixcelNum > 1000) {  // ピクセル数が800以上なら有と判定(灰)
      document.querySelector("body").style.backgroundColor = "#555"; 
    }else { // ピクセル数が800未満なら無と判定(黒)
      document.querySelector("body").style.backgroundColor = "#222";     
    }
    drawGrayImg(diff0, ctx, imgData); 						// 表示する
    var tmp = gray[0]; 
    gray[0] = gray[1], gray[1] = gray[2], gray[2] = tmp; // 前につめ直す
    delete pixcelNum; 											//バッファクリア
  };
}
