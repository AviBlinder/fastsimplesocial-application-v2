function ShowDateTime() {
    
    var question_pk = $("#question_pk").html() 

    $.ajax({
        url: $("#UpdateDateTime").attr("date-time-url"),
       data: {
          'pk': question_pk
        },

        dataType: 'json',
        success: function (data) {
          if (data.due_date) {
                $("#id_due_day").val(data.due_date) ;
          } else {
            var current_date = moment().format("YYYY-MM-DD")      ;
            $("#id_due_day").val(current_date) ;
              }
            if (data.due_time) {
                $("#id_due_time").val(data.due_time) ;
          } else {
               var current_time = moment().format("HH:mm")      ;
                $("#id_due_time").val(current_time)
              }
        },
          error: function(data){
                var current_date = moment().format("YYYY-MM-DD")      ;
                $("#id_due_day").val(current_date) ;
                var current_time = moment().format("HH:mm")      ;
                $("#id_due_time").val(current_time);

             }
      });

    $("#UpdateDateTime").toggle();

}
