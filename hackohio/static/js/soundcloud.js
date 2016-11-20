window.soundcloud = new function() {

    var This = this;

    this.getTracks = function(playlist_id, callback) {
        var url = "https://api-v2.soundcloud.com/playlists/" + playlist_id;

        var params = {
            representation: "full",
            client_id: window.soundcloudClientId,
            app_version: 1479467323
        };

        $.get(url, params, function(data, status, xhr) {
            console.log(data);
        });

    };

    window.addEventListener("load", function(ev) {
        This.getTracks(271195793, null);
    });
}();
