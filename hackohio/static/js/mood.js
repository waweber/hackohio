window.mood = new function(){
    this.updateMode = "webcam";
    this.twitterHandle = "librewulf";

    var This = this;

    this.setMood = function(mood) {
        console.log("Mood: " + mood);
        window.music.getPlaylist(mood, window.music.queuePlaylist);

        $(".glowy").removeClass("happy");
        $(".glowy").removeClass("sad");
        $(".glowy").removeClass("angry");

        if (mood == "happy" || mood == "sad" || mood == "angry")
            $(".glowy").addClass(mood);
    };

    this.updateMood = function() {
        if (This.updateMode == "twitter") {
            $.get("/mood/twitter", {
                handle: This.twitterHandle
            }, function(data, status, xhr) {
                if (data.mood == "happy") {
                    This.setMood("happy");
                } else if (data.mood == "sad") {
                    This.setMood("sad");
                } else if (data.mood == "angry") {
                    This.setMood("angry");
                } else if (data.mood == "neutral") {
                    This.setMood("neutral");
                }
            });
        } else if (This.updateMode == "webcam") {
            window.camera.takePicture(function(text) {
                if (text == "happy") {
                    This.setMood("happy");
                } else if (text == "sad") {
                    This.setMood("sad");
                } else if (text == "angry") {
                    This.setMood("angry");
                } else if (text == "neutral") {
                    This.setMood("neutral");
                }
            });
        }
    };

    window.addEventListener("load", function(ev) {
        window.setInterval(function(ev) {
            This.updateMood();
        }, 15000);
    });

}();
