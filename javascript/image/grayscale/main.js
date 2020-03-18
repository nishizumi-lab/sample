// グレースケール変換
var colorToGray = function(src, dst, w, h) {
    for (var i = 0; i < h; i++) {
        for (var j = 0; j < w; j++) {
            var p = (i*w+j)*4;
            var val =  0.299*src[p] + 0.587*src[p+1] + 0.114*src[p+2];
            dst[p] = val;
            dst[p + 1] = val;
            dst[p + 2] = val;
            dst[p + 3] = src[p + 3];
        }
    }
};
 
window.addEventListener("DOMContentLoaded", function(){
    var ofd = document.getElementById("selectfile");
    // ファイルを開いた時の処理
    ofd.addEventListener("change", function(evt) {
        var im = null;
        var cvs = document.createElement("canvas");
        var file = evt.target.files;
        var reader = new FileReader();
        //　dataURL形式でファイルの取得
        reader.readAsDataURL(file[0]);
        // ファイルの取得が完了した時の処理
        reader.onload = function(){
            im = new Image();
            im.onload = function(){
                // 画像をcanvasにセット
                var ctx = cvs.getContext('2d');
                var w = im.width;   // 入力画像の幅
                var h = im.height;  // 入力画像の高さ
                cvs.width = w;
                cvs.height = h;
                // 入力画像のデータを取得
                ctx.drawImage(im, 0, 0);
                var im1Data = ctx.getImageData(0, 0, w, h);
                // 入力画像と同じサイズの配列生成(出力画像用)
                var im2Data = ctx.createImageData(w,h);
                var im1 = im1Data.data;
                var im2 = im2Data.data;
                // 画像データのグレースケール変換
                colorToGray(im1, im2, w, h);
                // 出力画像をCamvusに配置
                ctx.putImageData(im2Data, 0, 0);
                document.getElementById("dispimg").innerHTML = "";
            };
            im.src = reader.result;
        };
    }, false);
});
