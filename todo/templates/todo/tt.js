        $.get('?page=2')
            .done((html) => {
                console.log("얻어온 html으로 화면을 바꿔 치기 ");
                console.log("html : ", html)
                $('#post-list-wrapper').html(html)
            })
            .fail(() => {
                console.log("fail");
            })
            .always(() => {
                console.log('always');
            })
            $('.modal22').removeAttr('hidden');
            $( ".modal22" ).modal('show');
            $(".modal22").css("z-index", "1500");
        // $( this ).text( htmlString );
    })