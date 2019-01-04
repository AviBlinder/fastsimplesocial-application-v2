function DeleteAnswer(loopNumber,answer_pk) {
  
            $.ajax({
                url: $("#delete-answer-url").attr("delete-answer-url"),
                data: {
                  'answer_pk': answer_pk,
                },
                
                dataType: 'json',
                success: function (data) {
                  if (data.result == 'true') {
                    var removed_answer = ".answer_loop" + loopNumber
                      $(removed_answer).remove()
                  }
                },
                error: function(data) {
                 console.log("error in DeleteAnswer") 
                }
           });
}
