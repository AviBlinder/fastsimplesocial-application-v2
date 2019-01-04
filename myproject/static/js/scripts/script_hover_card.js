    $(document).ready(function() {

        $(".question_card").hover(
            function() {
                $(this).animate({
                 marginTop:'-=1%'
                }, 'fast');
            },
            function() {
                $(this).animate({
                 marginTop:'0%'
                }, 'fast');
            });
    });
