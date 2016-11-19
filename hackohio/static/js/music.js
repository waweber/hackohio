
window.music = new function () {

    var This = this;

    this.currentPlaylist = [];
    this.analyser = null;

    this.playToggle = function(element) {
        if ($(element).hasClass("glyphicon-play")) {
            $(element).removeClass("glyphicon-play");
            $(element).addClass("glyphicon-pause");
            $("#media")[0].play();
        } else if ($(element).hasClass("glyphicon-pause")) {
            $(element).removeClass("glyphicon-pause");
            $(element).addClass("glyphicon-play");
            $("#media")[0].pause();
        }
    };

    this.play = function(songInfo) {
        $("#songTitle").html(songInfo.title);
        $("#artistName").html(songInfo.artist);
        $("#albumName").html(songInfo.album);
        $("#albumArt").attr("src", songInfo.cover);
        $("#media").attr("src", songInfo.media);
        $("#media")[0].load();
        $("#media")[0].play();

        if ($(".playbtn").hasClass("glyphicon-play")) {
            $(".playbtn").removeClass("glyphicon-play");
            $(".playbtn").addClass("glyphicon-pause");
        }

        if (Notification.permission != "granted") {
            Notification.requestPermission();
        }

        new Notification(
            "Now Playing: " + songInfo.title + " by " + songInfo.artist,
            {
                icon: songInfo.cover
            }
        );
    };

    this.queuePlaylist = function(playlist) {
        This.currentPlaylist = playlist;

        This.play(This.currentPlaylist.shift());
    };

    this.advancePlaylist = function() {
        if (This.currentPlaylist.length > 0) {
            var song = This.currentPlaylist.shift();
            This.play(song);
        };
    };

    this.getPlaylist = function(mood, callback) {
        $.get("/playlist/" + mood, null, function(data, status, xhr) {
            callback(data);
        });
    };

    var renderAnalyser = function() {
        var freqData = new Uint8Array(This.analyser.frequencyBinCount);
        This.analyser.getByteFrequencyData(freqData);

        var avgFreqData = new Float32Array(50);

        for (var i = 0; i < 50; i++) {
            var minIdx = i * Math.floor(freqData.length / avgFreqData.length);
            var maxIdx = minIdx + Math.floor(freqData.length /
                    avgFreqData.length) - 1;

            if (maxIdx >= freqData.length)
                maxIdx = freqData.length - 1;

            var count = maxIdx - minIdx + 1;

            avgFreqData[i] = 0;

            for (j = minIdx; j <= maxIdx; j++) {
                avgFreqData[i] += freqData[j];
            }

            avgFreqData[i] /= count;
        }

        console.log(avgFreqData);
    };

    this.attachAnalyser = function(element) {
        var ctx = new AudioContext();
        var src = ctx.createMediaElementSource(element);
        var analyser = ctx.createAnalyser();

        This.analyser = analyser;

        console.log(analyser.fftSize);
        analyser.fftSize = 2048;

        src.connect(analyser);

        window.setInterval(function (ev) {
            renderAnalyser();
        }, 100);
    };

    document.addEventListener("click", function(ev) {
        if (ev.target.className.indexOf("playbtn") != -1) {
            This.playToggle(ev.target);
        } else if (ev.target.className.indexOf("glyphicon-step-forward") != -1) {
            This.advancePlaylist();
        }
    });

}();
