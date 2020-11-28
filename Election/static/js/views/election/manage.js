$(function() {

    var doubleSubmit = false;

    $('#add_voter_btn').click(function(event) {
        console.log('test');
        var btn = $(this);
        var modal = $('#addVoterModal');
        modal.modal('show');
    });

    $('#addVoterModal').ajaxForm({
        beforeSubmit: function(data) {
            if(!doubleSubmit) {
                doubleSubmit = true;
            } else {
                console.log("중복 클릭");
                return false;
            }
        },
        success: function(data) {
            alert("성공");
            location.reload();
            //location.href = flask_util.url_for('election_page.manageElection');
        },
        error: function(data) {
            alert("실패.");
            doubleSubmit = false;
        }
    });

    $("#lookupvotersbtn").click(function(){


        if(result){
            $.ajax({
                type:"DELETE",
                url: "/modifyElection/" + id
            })
            .done(function(data){
                alert(start + '~' + end + " 삭제 되었습니다.");
                location.href = "/bingo_event/";
            })
            .fail(function(data){
                if(data.status == 403)
                {
                    alert("수정권한이 없습니다.");
                }
                else {
                    alert("failed");
                    console.log(data);
                }
            });
        }
        else{
            console.log('break false');
        }
    });
})
