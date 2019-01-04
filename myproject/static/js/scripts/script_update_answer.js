function UpdateAnswer(answer_pk,forloopNumber) {
  
            var new_answer_content = $("#input_updated_answer input").val() 

            $.ajax({
                url: $("#update-answer-url").attr("update-answer-url"),
                data: {
                  'answer_pk': answer_pk,
                  'new_answer_content' : new_answer_content
                },
                
                
                dataType: 'json',
                success: function (data) {
                  if (data.result == 'true') {
                     answer_content_id = "#answer_" + forloopNumber + ' h5'
                     $(answer_content_id).text(data.updated_answer)

                  }
                     remove_input_answer(forloopNumber);

                }
           });
  