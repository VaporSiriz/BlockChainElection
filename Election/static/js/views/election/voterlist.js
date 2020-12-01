$(function(){
    $('.apply-voter').click(function(){
        var election_id = $(this).data("election-id");
        var conf = prompt("후보자 신청을 하시겠습니까?");
        if(conf)
        {
            location.href=flask_util.url_for('election_page.voter_list', {election_id:election_id});
        }
    })
})
