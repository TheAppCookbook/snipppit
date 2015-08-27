// Live Feedback
function forgot_password() {
    $("#fname").hide();
    $("#lname").hide();
    $("#email").show();
    $("#pword").hide();
    
    $("#forgot_password").hide();
    $("#sign_up_l").show();
    
    $("#log_in").show();
    $("#sign_up_r").hide();
    
    $("#form").attr("action", "/forgot");
    $("#form").attr("method", "GET");
}

function log_in() {
    $("#fname").hide();
    $("#lname").hide();
    $("#email").show();
    $("#pword").show();
    
    $("#forgot_password").show();
    $("#sign_up_l").hide();
    
    $("#log_in").hide();
    $("#sign_up_r").show();
    
    $("#form").attr("action", "/login");
    $("#form").attr("method", "POST");
}

function sign_up() {
    $("#fname").show();
    $("#lname").show();
    $("#email").show();
    $("#pword").show();
    
    $("#forgot_password").show();
    $("#log_in").show();
    
    $("#sign_up_l").hide();
    $("#sign_up_r").hide();
    
    $("#form").attr("action", "/login");
    $("#form").attr("method", "POST");
}

$(function () {
    $("#sign_up_l").hide();
    $("#sign_up_r").hide();
});