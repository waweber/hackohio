$(function() {
    "use strict";

    $('#twitterDet').change(function() {
        $('#twitterHandle').removeClass('invisible');
    });

    $('#webcamDet').change(function() {
        $('#twitterHandle').addClass('invisible');
    });

    $('#settingsSave').click(function() {
        var selected = $('input[name=determiner]:radio:checked')[0];

        if (selected !== undefined) {
            if (selected.id === 'twitterDet') {
                window.mood.updateMode = "twitter";
                window.mood.twitterHandle = $('#twitterHandle input').val();
            }
            else if (selected.id === 'webcamDet') {
                window.mood.updateMode = "webcam";
                window.mood.twitterHandle = undefined;
            } else {
                window.mood.updateMode = undefined;
                window.mood.twitterHandle = undefined;
            }

            $('#settingsModal').modal('toggle');
        }
    });

});
