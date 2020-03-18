// フィルタ処理
var filter2d = function(src, dst, w, h, kernel) {
    for (var i = 0; i < h; i++) {
        for (var j = 0; j < w; j++) {
            var dx = (j + i * w) * 4;
            var val = [0,0,0];
            for(var k = -1; k <= 1; k++){
                for(var l = -1; l <= 1 ; l++){
                    var x = j + l;
                    var y = i + k;
                    if(x < 0 || x >= w || y < 0 || y >= h){
                        continue;
                    }
                    var dx1 = (x + y * w) * 4;
                    var dx2 = (l + 1) + (k + 1)*3;
                    val[0] += kernel[dx2]*src[dx1];
                    val[1] += kernel[dx2]*src[dx1 + 1];
                    val[2] += kernel[dx2]*src[dx1 + 2];
                }
            }
            dst[dx] = val[0];
            dst[dx + 1] = val[1];
            dst[dx + 2] = val[2];
            dst[dx + 3] = src[dx + 3];
        }
    }
};


window.addEventListener("DOMContentLoaded", function(){
    var ofd = document.getElementById("selectfile");
    // ファイルを開いた時の処理
    ofd.addEventListener("change", function(evt) {
        var im = null;
        var canvas = document.createElement("canvas");
        var file = evt.target.files;
        var reader = new FileReader();
        //　dataURL形式でファイルの取得
        reader.readAsDataURL(file[0]);
        // ファイルの取得が完了した時の処理
        reader.onload = function(){
            im = new Image();
            im.onload = function(){
                // 画像をcanvasにセット
                var context = canvas.getContext('2d');
                var w = im.width;   // 入力画像の幅
                var h = im.height;  // 入力画像の高さ
                canvas.width = w;
                canvas.height = h;
                context.drawImage(im, 0, 0);

                // 入力画像のデータを取得
                var im1Data = context.getImageData(0, 0, w, h);
                // 入力画像と同じサイズの配列生成(出力画像用)
                var im2Data = context.createImageData(w, h);
                var im1 = im1Data.data;
                var im2 = im2Data.data;
                // Sobelフィルタのカーネル
                var kernel = [-1,0,1,
                              -2,0,2,
                              -1,0,1];
                // Sobelフィルタでエッジ抽出
                filter2d(im1, im2, w, h, kernel);
                // 出力画像をCamvusに配置
                context.putImageData(im2Data, 0, 0);
                //　出力画像のURLをセット
                document.getElementById("dispimg").innerHTML = "<img src='" + canvas.toDataURL() + "'>";
            }
            im.src = reader.result;
        }
    }, false);
});
