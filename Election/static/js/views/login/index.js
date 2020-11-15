$(function () {

    var doubleSubmit = false;

    $('#loginForm').ajaxForm({
        beforeSubmit: function(data){
            if(!doubleSubmit) {
                doubleSubmit = true;
            } else {
                console.log("중복 클릭");
                return false;
            }
        },
        success: function(data) {
            alert("성공");
            location.href = flask_util.url_for('login_page.status');
        },
        error: function(data) {
            alert("실패.");
            doubleSubmit = false;
        }
    })
})