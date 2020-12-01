$(function () {
    $('#btn_login').click(function() {
        $.ajax({
            url: flask_util.url_for('login_page.login'),
            type: 'POST',
            success: function (response) {
                console.info(response);
                alert("성공");
                location.href = flask_util.url_for('index_page.index');                
            },
            error: function (error) {
                console.error(error);
            }
        })
    })
})