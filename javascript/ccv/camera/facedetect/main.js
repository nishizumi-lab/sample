var video = document.getElementById("world");
var dispCs = document.getElementById("disp");

function start() {
    if(navigator.webkitGetUserMedia) {
        navigator.webkitGetUserMedia({audio:false, video:true}, function(stream) {
	    var url = window.webkitURL.createObjectURL(stream);
	    video.src = url;
	    myDraw();
        },function (error){});
    }else if(navigator.mozGetUserMedia){
        navigator.mozGetUserMedia(
            {video: true},
            function(stream) {
                video.mozSrcObject=stream;
                video.play();
                streaming = true;
                myDraw();
            },
            function(err) {
                alert("An error occured! " + err);
            }
        );
    } else if(navigator.getUserMedia) {
        navigator.getUserMedia("audio, video", success, error);
    }
}

function myDraw() {
    var hiddenCanvas = document.createElement('canvas');
    hiddenCanvas.width = video.videoWidth/2;
    hiddenCanvas.height = video.videoHeight/2;
    console.log("hiddenCanvas.width = "+hiddenCanvas.width);
    console.log("hiddenCanvas.height = "+hiddenCanvas.height);
    if(hiddenCanvas.width===0) {
	    setTimeout(myDraw, 1000);
	    return;
    }
    var ctx = hiddenCanvas.getContext('2d');
    ctx.drawImage(video,0,0,hiddenCanvas.width,hiddenCanvas.height);
    dispCs.width=video.videoWidth/2;
    dispCs.height=video.videoHeight/2;
    ctx = dispCs.getContext('2d');
    ctx.drawImage(video,0,0,dispCs.width,dispCs.height);
    var s = (new Date()).getTime();
    // 顔検出
    var comp = ccv.detect_objects({
	      "canvas" :ccv.grayscale(hiddenCanvas),
        "cascade": cascade,
        "interval": 5,
        "min_neighbors": 1
    });
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#f00";
    for (var i = 0; i < comp.length; i++) {
        ctx.strokeRect(comp[i].x, comp[i].y, comp[i].width, comp[i].height);
    }
    setImmediate(myDraw);
}

function stop() {
    if(navigator.webkitGetUserMedia) {
      navigator.webkitGetUserMedia({audio:true, video:true}, function(stream) {
	    stream.stop();
      });
      video.src=null;
    }
}
