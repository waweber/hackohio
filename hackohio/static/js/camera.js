window.camera = new function() {
    this.takePicture = function() {
        Webcam.snap(function(data_uri) {
            Webcam.upload(data_uri, "/mood/webcam", function(code, text) {
                console.log(text);
            });
        });
    };

    window.addEventListener("load", function(ev) {
        Webcam.set({
            width: 600,
            height: 450,
            fps: 1
        });
        Webcam.attach("#cameraplaceholder");
    });
}();
