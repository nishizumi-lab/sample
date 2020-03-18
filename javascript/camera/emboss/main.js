// 画像のフィルタ処理
function filter2d(src, dst, w, h, k, type) {
    var x, y, i;
    var p11, p12, p13, p21, p22, p23, p31, p32, p33;
    // 入力がグレースケール画像の場合
    if(type == '0'){
        for (y=1; y<h; y++) {
            for (x=1; x<w; x++) {
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
        for (y=1; y<h; y+= 4) {
            for (x=1; x<w; x+= 4) {
                i = x+y*w;
                for (var v=0; v<3; v++) {
                    p11 = src[x-1+(y-1)*w+v];
                    p12 = src[x +(y-1)*w+v];
                    p13 = src[x+1+(y-1)*w+v];
                    p21 = src[x-1+(y )*w+v];
                    p22 = src[i+v];
                    p23 = src[x+1+(y )*w+v];
                    p31 = src[x-1+(y+1)*w+v];
                    p32 = src[x +(y+1)*w+v];
                    p33 = src[x+1+(y+1)*w+v];
                    // 畳み込み演算
                    dst[i+v] = p11*k[0] + p12*k[1] + p13*k[2] +p21*k[3] + p22*k[4] + p23*k[5] +p31*k[6] + p32*k[7] + p33*k[8];
                }
                dst[i+3] = 255;
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
        context.putImageData(imdata, 0, 0);
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
    var gray = new Uint8ClampedArray(w*h);          // グレースケール画像格納
    var edge = new Uint8ClampedArray(w*h);			// 出力画像格納用
    var btnflag = true;                             // ボタンの判定
    var kernel = [1, 0,-1,							// フィルタのカーネル
                  1, 0,-1,
                  1, 0,-1];
 
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
        ctx.drawImage(video, 0, 0, w, h);       // 動画のフレームをcanvusに描画
        var im = ctx.getImageData(0, 0, w, h);  // canvusから画像データを取得
        cvtColor(im.data, gray, 0);             // カラー画像をグレースケールに変換
        filter2d(gray, edge, w, h, kernel, 0);	// グレースケール画像にフィルタ処理
        requestAnimationFrame(onFrame);         // 再帰
        imshow(im, edge, ctx, 0);				// 画像を描画   
    };
}
