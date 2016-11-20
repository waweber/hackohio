window.soundcloud = new function() {

    var This = this;

    

    this.getTracks = function(playlist_id, callback) {
        var url = "/soundcloud/tracks"

        var params = {
            playlist_id: playlist_id
        };

        $.get(url, params, function(data, status, xhr) {
            callback(data);
        });

    };

    this.trackToPlaylistItem = function(track) {

        var cover = track.artwork_url || track.user.avatar_url;

        cover = cover.replace("large", "t500x500")

        return {
            artist: track.user.username,
            album: "",
            title: track.title,
            cover: cover,
            track_id: track.id
        }
    };

    this.buildPlaylist = function(tracks) {
        var playlist = [];

        for (var i in tracks) {
            playlist.push(This.trackToPlaylistItem(tracks[i]));
        }

        return playlist;
    };

    this.playTrackId = function(track_id, playCallback) {
        var url = "/soundcloud/file?track_id=" + track_id;
        playCallback(url);
    };

    this.queuePlaylist = function(mood) {
        var id;
        if (mood == "happy") {
            id = 276991253;
        } else if (mood == "sad") {
            id = 276989807;
        } else if (mood == "angry") {
            id = 276990583;
        } else {
            id = 276992887;
        }


        This.getTracks(id, function(tracks) {
            var pls = This.buildPlaylist(tracks);
            window.music.queuePlaylist(pls);
        });

    };

    window.addEventListener("load", function(ev) {
        This.queuePlaylist("neutral");
    });
}();
