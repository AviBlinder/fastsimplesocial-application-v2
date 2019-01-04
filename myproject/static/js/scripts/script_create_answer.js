function CreateAnswer(question_answers) {
            var new_question_answers = $('.answer_item').length + 1

            var question_pk = $("#question_pk").html() 
            
            var answer = $('#new_answer').val()
            
            $.ajax({
                url: $("#create-answer-url").attr("create-answer-url"),
                data: {
                  'pk': question_pk,
                  'answer': answer
                },

                dataType: 'json', 
                success: function  (data) {
                  if (data.result == 'true' && data.created == 1) {
                        var last_answer_number = data.new_answer_counter - 2
                        if (last_answer_number < 0){
                            last_answer_number = 0
                        }
                        console.log("last_answer_number (index 0) = "+ last_answer_number)
                        var new_answer_number = data.new_answer_counter - 1
				

                var firstDiv = '<div class="answer_loop' + new_question_answers + '">' +
                '\t <div class="mt-1 px-sm-2 sm-2  ' +
                                        ' answer_item ">' + '\n' +
                                '\t <div class="d-flex flex-row "> \n' + 
                                '\t <span id="answer_' + new_question_answers + '"> \n' +
                                '\t \t <h5> '  +  data.new_answer + '\n' + '\t </h5> </span> \n'  


                var EditAnswerButton = 
                '\t <button class="ml-2"  onclick="AnswerToggle(forloopNumber='  + new_answer_number + ')" \n ' + 
                            '\t \t style="border: none; background:none;font-size:0.8em;color:CadetBlue ;"> \n' + 
                           '\t \t \t <i class="fa fa-edit "></i> \n \t </button> \n';
						'\t<button onclick="AnswerToggle(forloopNumber= \n' + 
						new_question_answers + ' ,answer_pk=\n' + 
						data.new_answer_pk + ')"\n '  +  
						   '\t style="border: none; background:none;font-size:0.8em;color:CadetBlue;"> \n' +
									 '\t \t <i class="fa fa-edit"></i> \n' + 
								'</button> \n'

                var DeleteAnswerButton = 	'\t <button ' +
                            'onclick="DeleteAnswer(loopNumber=' + 
                            new_question_answers + ', answer_pk=' + 
                            data.new_answer_pk +  ')" \n ' + 
                            '\t \t style="border: none; background:none;font-size:0.8em;color:CadetBlue ;"> \n' + 
                           '\t \t \t <i class="fa fa-eraser "></i> \n' 
                           + ' \t </button> \n';
                var EndFlex = '\t </div> \n'
                

                var hiddenDiv = ' \t <div class="form-group form-group' + new_question_answers +  ' form-inline" \n' + 
							  ' \t \t id="edit_answer' + new_question_answers + '" style="display:none;">\n' +
							 ' \t \t <input type="text" class="form-control form-control-sm "  \n' +
		       	              ' \t \t \t    name="new_answer' + new_question_answers + '" id="new_answer' + 
		       	                new_question_answers + '" /> \n' +
							' \t \t <button onclick="UpdateAnswer(forloopNumber=' + 
							new_question_answers + 
							        ', answer_pk=' + data.new_answer_pk + ')" \n' +  
								' \t \t \t style="border: none; background:none;font-size:0.8em;color:CadetBlue;"> \n' +
								' \t \t \t \t <i class="fa fa-check-square-o fa-lg"  style="color:green;"></i>\n' +
								' \t \t </button> \n'
                var lastDivs = ' \t \t  </div> \t  </div> \n   </div>'
                
                    console.log(
                       firstDiv + 
                       EditAnswerButton + 
                       DeleteAnswerButton +     
                       EndFlex +                       
                       hiddenDiv +
                       lastDivs
                        )


                    var new_answer_number_class = ".answer_loop" + $('.answer_item').length
                    
                    // $('.answer_loop').eq(data.new_answer_counter - 1).parent('div').append(
                    $(new_answer_number_class).append(

                        firstDiv + 
                       EditAnswerButton + 
                       DeleteAnswerButton + 
                       EndFlex +                       
                       hiddenDiv +
                       lastDivs
                       )
                  }
                  $('#new_answer').remove();
                  $('#addanswer').remove();
                  $('#deleteanswer').remove();
                }
           });
        
}
