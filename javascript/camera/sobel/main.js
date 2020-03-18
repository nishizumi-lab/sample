// 画像のフィルタ処理
function filter2d(src, dst, w, h, k, type) {
    var x, y, i;
    var p11, p12, p13, p21, p22, p23, p31, p32, p33;
    // 入力がグレースケール画像の場合
    if(type == '0'){
        for (y=1; y<h-1; y++) {
            for (x=1; x<w-1; x++) {
                i = x+y*w;
                p11 = src[x-1+(y-1)*w];
                p12 = src[x +(y-1)*w];
                p13 = src[x+1+(y-1)*w];
                p21 = src[x-1+(y )*w];
                p22 = src[i              ];
                p23 = src[x+1+(y )*w];
                p31 = src[x-1+(y+1)*w];
                p32 = src[x +(y+1)*w];
                p33 = src[x+1+(y+1)*w];
                // 畳み込み演算
                dst[i] = p11*k[0] + p12*k[1] + p13*k[2] +p21*k[3] + p22*k[4] + p23*k[5] +p31*k[6] + p32*k[7] + p33*k[8];
            }
        }
    }
    // 入力がカラー画像の場合
    else if(type == '1'){
        for (i = 0; i < h; i++) {
            for (j = 0; j < w; j++) {
                var dx = (j + i * w) * 4;
                var val = [0,0,0];
                for(var v = -1; v <= 1; v++){
                    for(var l = -1; l <= 1 ; l++){
                        x = j + l;
                        y = i + v;
                        if(x < 0 || x >= w || y < 0 || y >= h){
                            continue;
                        }
                        var dx1 = (x + y * w) * 4;
                        var dx2 = (l + 1) + (v + 1)*3;
                        val[0] += k[dx2]*src[dx1];
                        val[1] += k[dx2]*src[dx1 + 1];
                        val[2] += k[dx2]*src[dx1 + 2];
                    }
                }
                dst[dx] = val[0];
                dst[dx + 1] = val[1];
                dst[dx + 2] = val[2];
                dst[dx + 3] = src[dx + 3];
            }
        }
    }
}
  
// 画像の色空間を変換
function cvtColor(src, dst, type) {
    // 入力がグレースケール画像の場合
    if(type == '0'){
        for (var i = 0; i < src.length; i += 4) {
            dst[i/4] = 0.299*src[i+0] + 0.587*src[i+1] + 0.114*src[i+2];
        }
    }
    else if(type == '1'){
    }
}
  
// 画像の描画
function imshow(imdata, im, ctx, type){
    // 入力がグレースケール画像の場合
    if(type == '0'){
        var n = im.length*4;
        var color = new Uint8ClampedArray(n);
        for (var i = 0; i < n; i += 4){
            color[i+0] = im[i/4];
            color[i+1] = im[i/4];
            color[i+2] = im[i/4];
            color[i+3] = 255;
        }
        imdata.data.set(color);
        ctx.putImageData(imdata, 0, 0);
    }
    // 入力がカラー画像の場合
    else if(type == '1'){
        imdata.data.set(im);
        ctx.putImageData(imdata, 0, 0);
    }
}
  
// カメラ映像の描画
function showVideo(){
    // 変数の定義
    var cvs = document.getElementById("cv");
    var ctx = cvs.getContext("2d");
    var btn = document.getElementById("btn");       //ボタンハンドラ
    var video = document.getElementById("video");   //ビデオハンドラ
    var w = cvs.width;                              // canvusの幅
    var h = cvs.height;                             // canvusの高さ
    var edge = new Uint8ClampedArray(w*h*4);		// 出力画像格納用
    var btnflag = true;                             // ボタンの判定
    var kernel = [-1, 0, 1,                         // フィルタのカーネル
                  -2, 0, 2,
                  -1, 0, 1];
  
    // Videoタグ
    navigator.getMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
    navigator.getMedia ({ video:true, audio:true }, function(stream) { video.src = window.URL.createObjectURL(stream); }, function(err){console.log(err);});
  
    //ボタンイベント処理
    btn.onclick = function(){
        if (btnflag) {
            video.play();                   // ビデオ再生
            requestAnimationFrame(onFrame); // カメラ映像の表示開始
            btnflag = false;
        }
    };
  
    // 繰り返し行う処理
    var onFrame = function () {
        ctx.drawImage(video, 0, 0, w, h);			// 動画のフレームをcanvusに描画
        var im = ctx.getImageData(0, 0, w, h);		// canvusから画像データを取得
        filter2d(im.data, edge, w, h, kernel, 1);	// 画像にフィルタ処理
        requestAnimationFrame(onFrame);				// 再帰
        imshow(im, edge, ctx, 1);					// 画像を描画  
    };
}
