var players = [];

function onYouTubeIframeAPIReady() {
    var playerElements = document.querySelectorAll('div[id^="player"]');
    playerElements.forEach(function(element, index) {
        var videoUrl = element.getAttribute('videoUrl');
        var start = parseTime(element.getAttribute('start'));
        var end = parseTime(element.getAttribute('end'));
        var height = element.getAttribute('height');
        var width = element.getAttribute('width');

        players[index] = new YT.Player(element.id, {
            height: height,
            width: width,
            videoId: getVideoId(videoUrl),
            playerVars: {
                start: start,
                end: end,
                loop: 1,
                playlist: getVideoId(videoUrl)
            },
            events: {
                'onReady': function(event) {
                    onPlayerReady(event, start);
                },
                'onStateChange': function(event) {
                    onPlayerStateChange(event, start, end);
                }
            }
        });
    });
}

function parseTime(time) {
    var parts = time.match(/(\d+)(s|m|h)/);
    var value = parseInt(parts[1]);
    var unit = parts[2];
    if (unit === 'h') {
        return value * 3600;
    } else if (unit === 'm') {
        return value * 60;
    } else {
        return value;
    }
}

function getVideoId(url) {
    var match = url.match(/v=([^&]+)/);
    return match ? match[1] : null;
}

function onPlayerReady(event, start) {
    event.target.seekTo(start);
    event.target.playVideo();
}

function onPlayerStateChange(event, start, end) {
    if (event.data === YT.PlayerState.ENDED) {
        event.target.seekTo(start);
        event.target.playVideo();
    } else if (event.data === YT.PlayerState.PLAYING) {
        var checkTime = function() {
            if (event.target.getCurrentTime() >= end) {
                event.target.seekTo(start);
            } else {
                setTimeout(checkTime, 100);
            }
        };
        setTimeout(checkTime, 100);
    }
}