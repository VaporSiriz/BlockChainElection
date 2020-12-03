$(function(){
    $('.card-btn').click(function(){
        var election_id = $(this).data("election-id");
        var func = $(this).data("func");
        //location.href="./voter.html";
        location.href=flask_util.url_for('election_page.voter_list', {election_id:election_id, func:func});
    })
})
