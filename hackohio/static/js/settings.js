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
                window.updateMode = "twitter";
                window.twitterHandle = $('#twitterHandle input').val();
            }
            else if (selected.id === 'webcamDet') {
                window.updateMode = "webcam";
            }

            $('#settingsModal').modal('toggle');
        }
    });

});
