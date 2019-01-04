function EditAnswer(question_answers) {
            console.log("CreateAnswer - question_answers=" + question_answers)
            

            var question_pk = $("#question_pk").html() 
            
            var answer = $('#new_answer').val()

            var button2 = 	'<button id="edit_new_answer" onclick="CreateAnswer()" ' + 
                            'style="border: none; background:none;font-size:0.8em;color:CadetBlue ;">' + 
                           '<i class="fa fa-edit "></i></button>';


            $.ajax({
                url: $("#create-answer-url").attr("create-answer-url"),
                data: {
                  'pk': question_pk,
                  'answer': answer
                },

                dataType: 'json',
                success: function (data) {
                  if (data.result == 'true') {
                      
                    var button3 = 	'<button ' +
                            'onclick="DeleteAnswer(loopNumber=' + 
                            question_answers + ',answer_pk=' + 
                            data.answer_pk + 
                            ') " style="border: none; background:none;font-size:0.8em;color:CadetBlue ;">' + 
                           '<i id="delete_button" class="fa fa-eraser "></i></button>';

                        console.log("CreateAnswer - question_answers=" + question_answers)


                        console.log('<div class="pt-3 answer_loop" ' + 
                       'id="answer_' + question_answers + '">' +  
                       data.answer + ' ' + button2 + ' ' + button3 + '</div>')
                       
                        var last_answer_number = data.new_answer_counter - 2
                        console.log("last_answer_number = "+ last_answer_number)

                    $('.answer_loop').eq(data.new_answer_counter - 2).parent('div').append(
                        '<div class="pt-3 answer_loop" ' + 
                       'id="answer_' + question_answers + '">' +  
                       data.answer + ' ' + button2 + ' ' + button3 + '</div>')
                  }
                  $('#new_answer').remove();
                  $('#addanswer').remove();
                  $('#deleteanswer').remove();
                }
           });
        
}

