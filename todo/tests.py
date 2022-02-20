from django.test import TestCase

# Create your tests here.
    var id;
    $("#todo_list a[class='title_for_list']").click(function(e){

        alert("삭제 버튼 클릭 2")

        e.preventDefault();
        window.history.pushState("", "", '/todo/')
        id = $(this).attr('id');

        // window.location.href = "www.daum.net";

        $.get(id)
            .done((html) => {
                console.log(html);
                $('#myModal_button').hide();
                $("#myModal").html(html)
                $( "#myModal_button" ).trigger( "click" );
            })
            .fail(() => {
                console.log("fail");
            })
            .always(() => {
                console.log('always');
            })
    });
