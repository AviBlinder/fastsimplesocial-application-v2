    function AddAnswer(question_answers) {

                var question_answers = question_answers
                var button1 = '<input type="text" autofocus autocomplete=off ' +
                        'class="mt-4 col-lg input-sm"  name="answer" ' + 
                 ' id=new_answer' + '> </input>';
 

 
                var button2 = ' <form action="/action_page.php" method="post"> \n' +
                ' \t <button type="submit" id="addanswer" \n ' + 
                ' \t \t  style="border: none; background:none;font-size:1em;color:CadetBlue ;"> \n ' + 
                ' \t \t \t <i class="fa fa-check mt-2"></i></button> \n' +
                '</form> \n' ; 
                var button3 = 	'<button id="deleteanswer"  ' + 
                            'style="border: none; background:none;font-size:1em;color:CadetBlue ;">' + 
                           '<i class="fa fa-close mt-2"></i></button>';

                $(".answer_button").attr('disabled',true)                

                 event.preventDefault();
                 
                $("#new_answer_item").append('<div id="extra_items" class="input-container mt-2">' +
                 button1 + '<div class="d-flex flex-row">' +  button2 + button3  + ' </div> </div>');
            };

            $('body').on('click', '#deleteanswer', function(e) {
                $(this).parent('div').parent('div').remove();
                $(".answer_button").attr('disabled',false)                
            });

    ; 
