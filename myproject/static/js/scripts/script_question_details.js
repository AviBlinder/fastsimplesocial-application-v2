$( document ).ready(function() {
   
    var current_time = moment().format("YYYY-MM-DD HH:mm")      ;

    var question_time = $('#question_due_date').html()
    // var question_time_formatted = moment(question_time).format("YYYY-MM-DD HH:mm")      ;

    var publish_result = question_time < current_time
    
    if (publish_result === true) {
        $("#show_question_results").css("display", "");
    } else {
        $("#dont_show_question_results").css("display", "");
    }     

});