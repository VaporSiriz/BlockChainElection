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
            console.log(data);
            alert(data);
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

    $("#startbtn").click(function(){
        var election_id = $(this).data("election-id");
        var result = confirm("지금 투표를 시작하시겠습니까?");
        if(result){
            $.ajax({
                type:"POST",
                url: flask_util.url_for('election_page.start_election', {election_id:election_id})
            })
            .done(function(data) {
                alert('선거가 시작 되었습니다.');
                location.reload();
            })
            .fail(function(data){
                if(data.status == 403)
                {
                    alert("수정권한이 없습니다.");
                }
                else {
                    alert(data.responseText);
                    console.log(data);
                }
            });
        }
    });

    $("#endbtn").click(function(){
        var election_id = $(this).data("election-id");
        var result = confirm("지금 투표를 시작하시겠습니까?");
        if(result){
            $.ajax({
                type:"POST",
                url: flask_util.url_for('election_page.start_election', {election_id:election_id})
            })
            .done(function(data) {
                alert('선거가 시작 되었습니다.');
                location.reload();
            })
            .fail(function(data){
                if(data.status == 403)
                {
                    alert("수정권한이 없습니다.");
                }
                else {
                    alert(data.responseText);
                    console.log(data);
                }
            });
        }
        else{
            console.log('cancel!');
        }
    });
})
