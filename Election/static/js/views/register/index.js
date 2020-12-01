$(function () {

    var doubleSubmit = false;

    $('#registerForm').ajaxForm({
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
            location.href = flask_util.url_for('login_page.index');
        },
        error: function(data) {
            alert(data.responseText);
            doubleSubmit = false;
        }
    })
})