function ShowMinAnswerers() {

    var question_pk = $("#question_pk").html() 

    $.ajax({
        url: $("#UpdateMinAnswerers").attr("min-answerers-url"),
       data: {
          'pk': question_pk
        },
        dataType: 'json',
        success: function (data) {

          if (data.min_answerers) {
                $("#id_min_answerers").val(data.min_answerers) ;
             } else {
                 $("#id_min_answerers").val(0);
             }
          },
          error: function(data){
              alert("error!!")
                $("#id_min_answerers").val(0);
             }
      });


    $("#UpdateMinAnswerers").toggle();
    
}
