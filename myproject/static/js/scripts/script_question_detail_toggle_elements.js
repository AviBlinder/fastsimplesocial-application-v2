function TogglePieChart(){
        $("#container").toggle();
    };
function ToggleResultsTable(){
        $("#ResultsTable").toggle();
    };

function AnswerToggle(forloopNumber,answer_pk){
    
    
        var answer_content_id = "#answer_" + forloopNumber;
        var answer_content = $(answer_content_id).text().trim();
        var edit_answer_button = "#edit_answer_button_" + forloopNumber

        $(edit_answer_button).attr('disabled',true)                
        
        var input_updated_answer = 
            ' <input  style="border: 1px solid green;" type="text" name="updated_answer" autofocus value="' + 
            answer_content + '" >';

		var button_ok = ' <button class="ml-2" ' +   
				'onclick="UpdateAnswer(answer_pk=' + answer_pk + 
				     ',forloopNumber=' + forloopNumber  + ')"' +  
                'style="border: none; background:none;font-size:0.8em;color:CadetBlue;">' + 
				' <i class="fa fa-check"></i>' + 
				'</button>'
				
        var button_cancel = '<button onclick="remove_input_answer(forloopNumber=' + forloopNumber + ')"' +  
						'style="border: none; background:none;font-size:0.8em;color:CadetBlue;">' + 
					    ' <i class="fa fa-close"></i>' + 
						' </button>  '
        
        var append_input = '<div id="input_updated_answer" >' +  input_updated_answer + 
                                    button_ok + button_cancel        +     '</div>'
        
        $(answer_content_id).parent('div').parent('div').append(append_input)


    };

    function remove_input_answer(forloopNumber){
                var edit_answer_button = "#edit_answer_button_" + forloopNumber
        
                $('#input_updated_answer').remove()
                $(edit_answer_button).attr('disabled',false)                
                
        };
  