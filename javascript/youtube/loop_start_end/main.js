var player;
function onYouTubeIframeAPIReady() {
    var playerElement = document.getElementById('player');
    var videoUrl = playerElement.getAttribute('videoUrl');
    var videoId = videoUrl.split('v=')[1];
    var startSeconds = parseTime(playerElement.getAttribute('start'));
    var endSeconds = parseTime(playerElement.getAttribute('end'));
    var height = playerElement.getAttribute('height') || '390';
    var width = playerElement.getAttribute('width') || '640';

    player = new YT.Player('player', {
        height: height,
        width: width,
        videoId: videoId, // 動画のIDをここに入れます
        events: {
            'onReady': function(event) {
                onPlayerReady(event, startSeconds);
            },
            'onStateChange': function(event) {
                onPlayerStateChange(event, startSeconds, endSeconds);
            }
        }
    });
}

function parseTime(timeStr) {
    var time = 0;
    var match = timeStr.match(/(\d+)([hms])/g);
    if (match) {
        match.forEach(function(part) {
            var unit = part.slice(-1);
            var value = parseInt(part.slice(0, -1));
            if (unit === 'h') {
                time += value * 3600;
            } else if (unit === 'm') {
                time += value * 60;
            } else if (unit === 's') {
                time += value;
            }
        });
    }
    return time;
}

function onPlayerReady(event, startSeconds) {
    // 動画の開始位置を設定
    player.seekTo(startSeconds);
    event.target.playVideo();
}

function onPlayerStateChange(event, startSeconds, endSeconds) {
    if (event.data == YT.PlayerState.PLAYING) {
        checkTime(startSeconds, endSeconds);
    }
}

function checkTime(startSeconds, endSeconds) {
    var currentTime = player.getCurrentTime();
    if (currentTime >= endSeconds) {
        player.seekTo(startSeconds);
    }
    setTimeout(function() {
        checkTime(startSeconds, endSeconds);
    }, 1000); // 1秒ごとにチェック
}