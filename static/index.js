;(function(window, $) {
    'use strict';

    $('#result-container').hide();

    var checkResult = function(jobId) {
        $.get('/result/' + jobId).done(function(res, status, xhr) {
            if (xhr.status === 202) {
                window.setTimeout(function() {
                    checkResult(jobId);
                }, 500);
            } else if (xhr.status == 200) {
                $('#result-text').show();
                $('#result-text').html(res.replace(/\n/g,'<br/>'));
                $('#progressbar').hide();

                var url = "https://twitter.com/intent/tweet?text=" + res;
                $("#share-container").empty().append( '<a class="twitter-share-button" href="' + url + '" data-size="large"> Tweet</a>' );
                twttr.widgets.load();
            }
        });
    };

    var requestEmoly = function(data) {
        $.post('/emoly', data).done(function(res) {
            window.setTimeout(function() {
                checkResult(res);
            }, 500);
        });
    };

    $('#emoly-btn').click(function() {
        $('#result-text').hide();
        $('#result-container').show();

        var data = { text: $('#textarea').val() };
        requestEmoly(data)
    });
})(this, jQuery);
