$(function(){

    var doubleSubmit = false;

    function getUrlParams() {
        var params = {};
        window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(str, key, value) { params[key] = value; });
        return params;
    }

    $('.voter-card_h').on("click",function() {
        $('.voter-card_h').removeClass('selected-voter');
        $(this).addClass('selected-voter');

    })

    $('.vote-btn').on("click",function(){
        let selected_voter = $('.selected-voter')
        let election_id = getUrlParams().election_id;
        let candidate_id = selected_voter.data('candidate-id');
        let candidate_name = selected_voter.data('candidate-name');
        console.log(candidate_id);
        if(candidate_id === undefined) {
            alert('후보를 선택해주세요!');
            return ;
        }

        let result = confirm(candidate_id + '번 ' + candidate_name + ' 후보에게 투표하시겠습니까?');

        if(result){
            if(!doubleSubmit) {
                doubleSubmit = true;
            } else {
                console.log("중복 클릭");
                return ;
            }
            $.ajax({
                type:"POST",
                url: flask_util.url_for('vote_page.vote'),
                data: {'election_id': election_id, 'candidate_id': candidate_id}
            })
            .done(function(data){
                alert("투표가 완료 되었습니다.");
                location.reload();
            })
            .fail(function(data){
                if(data.status == 403)
                {
                    alert("로그인이 필요합니다.");
                    doubleSubmit = false;
                }
                else {
                    alert(data.responseText);
                    doubleSubmit = false;
                    console.log(data);
                }
            });
        }
        else{
            doubleSubmit = false;
            console.log('break false');
        }

    })

    $('.btn-detail').on("click",function(){
        let election_id = getUrlParams().election_id;
        let candidate_id = $(this).data('candidate-id');
        location.href=flask_util.url_for('election_page.detail', {'election_id':election_id, 'candidate_id':candidate_id});
    })

    $('#myModal').on('shown.bs.modal', function () {
        $('#myInput').trigger('focus')
    })
})
