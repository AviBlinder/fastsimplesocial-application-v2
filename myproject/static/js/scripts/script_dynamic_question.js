        $(document).ready(function() {

            var question_number = 1;
            $("#add").click(function(e) {
                question_number += 1
                var button1 = '<input autofocus autocomplete=off ' + 
                'class ="mt-4 col-lg input-sm" type="text" name="answer"' + 
                question_number + 'id=answer' +  question_number + '> </input>';
                var button2 = '<input class="btn btn-success btn-md mt-2" type="button" value="add answer" id="addanswer" > </input>'
                var button3 = '<input class="btn btn-danger btn-md mt-2"  type="button" value="delete"    id="delete"> </input>';
                
                 event.preventDefault();
                $("#items").append('<div id="extra_items">' + button1 + button2 + button3 + '</div>');
            });

            $('body').on('click', '#delete', function(e) {
                $(this).parent('div').remove();
                question_number -= 1
            });

            $('body').on('click', '#addanswer', function(e) {
                question_number += 1
                var button1 = '<input autofocus autocomplete=off ' + 
                'class ="mt-4 col-lg input-sm" type="text" name="answer"' + 
                question_number + 'id=answer' + question_number + '> </input>';
                var button2 = '<input class="btn btn-success btn-md mt-2" type="button" value="add answer" id="addanswer" > </input>'
                var button3 = '<input class="btn btn-danger btn-md mt-2"  type="button" value="delete"    id="delete"> </input>';
                event.preventDefault();
                $("#items").append('<div id="extra_items">' + button1 + button2 + button3 + '</div>');
            });

        }); 