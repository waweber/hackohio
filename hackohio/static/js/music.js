
window.music = new function () {

    var This = this;

    this.currentPlaylist = [];

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

    document.addEventListener("click", function(ev) {
        if (ev.target.className.indexOf("playbtn") != -1) {
            This.playToggle(ev.target);
        } else if (ev.target.className.indexOf("glyphicon-step-forward") != -1) {
            This.advancePlaylist();
        }
    });

}();
