// Time
function seconds(time_str) {
    var pieces = time_str.split(':');
    return (parseInt(pieces[0]) * 60) + parseInt(pieces[1]);
}

function time_str(seconds) {
    var min = Math.floor(seconds / 60)
    var sec = (seconds % 60)
    
    return pad(min, 2) + ":" + pad(sec, 2);
}

// Formatting
function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

// Live Feedback
$(function () {
    // Countdown Label
    setInterval(function () {
        $(".count-down").each(function() {
            var value = seconds($(this).text()) - 1;
            if (value <= 0 || value == NaN) {
                $(this).parent().text($(this).attr("finished"));
                return;
            }
            
            $(this).text(time_str(value));
        });
    }, 1000);
});

function voteButtonWasPressed(postID) {
    $.post("/post/" + postID + "/vote", {}, function(response) {
        response = JSON.parse(response);
        var voteButtonID = "#vote_" + postID;
        
        var text = $(voteButtonID).text();
        var pieces = text.split('/');

        $(voteButtonID).text(response.votes + '/' + pieces[1]);
        $(voteButtonID).addClass('active');
        
        if (response.refresh) {
            location.reload();
        }
    });
}