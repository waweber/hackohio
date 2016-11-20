window.soundcloud = new function() {

    var This = this;

    this.getTracks = function(playlist_id, callback) {
        var url = "/soundcloud/tracks"

        var params = {
            playlist_id: playlist_id
        };

        $.get(url, params, function(data, status, xhr) {
            callback(data.tracks);
        });

    };

    this.trackToPlaylistItem = function(track) {
        return {
            artist: track.user.username,
            album: "",
            title: track.title,
            cover: track.artwork_url || track.user.avatar_url,
            track_id: track.id
        }
    };

    this.buildPlaylist = function(tracks) {
        var playlist = [];

        for (var i in tracks) {
            if (tracks[i]["user"])
                playlist.push(This.trackToPlaylistItem(tracks[i]));
        }

        return playlist;
    };

    this.playTrackId = function(track_id, playCallback) {
        var url = "/soundcloud/file?track_id=" + track_id;
        playCallback(url);
    };

    window.addEventListener("load", function(ev) {
        This.getTracks(271195793, function(tracks) {
            var playlist = This.buildPlaylist(tracks);
            window.music.queuePlaylist(playlist);
        });
    });
}();
