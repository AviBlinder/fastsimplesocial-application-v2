from django.http import JsonResponse

from models import Question,Answer,QuestionVotedByUser


def ajax_get_question_datetime(request):

    pk = request.GET.get('pk',None)

    try:
        question = Question.objects.get(pk=pk)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e)) 
        print "ajax_get_question_datetime except !"
 
    data = {
        'due_date':question.due_date.date(),
        'due_time':question.due_date.time()
    }
    
    return JsonResponse(data)
    
def ajax_get_question_min_answerers(request):

    pk = request.GET.get('pk',None)

    try:
        question = Question.objects.get(pk=pk)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e)) 
        print "ajax_get_question_datetime except !"
 
    data = {
        'min_answerers':question.min_answerers
    }
    
    return JsonResponse(data)    


def ajax_create_answer(request):
    pk = request.GET.get('pk',None)
    answer_text = request.GET.get('answer',None)
#    print "create answer params - pk = {} answer_text = {}".format(pk,answer_text)
    if answer_text == "":
        data = {
        'result': 'false'
        }
        return JsonResponse(data)    
    
    try:
        question = Question.objects.get(pk=pk)
#        answer = Answer.objects.
    
        new_answer, created = Answer.objects.get_or_create(question=question,answer = answer_text.encode('UTF-8'))
        if created:
            new_answer.save()

        new_answer_counter = question.answers.all().count()

        data = {
        'result': 'true',
        'new_answer': new_answer.answer,
        'new_answer_counter' : new_answer_counter ,
        'new_answer_pk' : new_answer.pk,
        'created' : created

        }

    except Exception as e:
        print '%s (%s)' % (e.message, type(e)) 
        print "ajax_create_answer except !"
        data = {
        'result': 'false'
        }
 
    return JsonResponse(data)    

def ajax_delete_answer(request):
    answer_pk = request.GET.get('answer_pk',None)
    # print "answer_pk = {}".format(answer_pk)
    

    try:
        answer = Answer.objects.get(pk=answer_pk)
        answer.delete()
        # print "answer deleted"
        data = {
        'result': 'true',
        'deleted_answer_pk' : answer_pk
        }

    except Exception as e:
        print '%s (%s)' % (e.message, type(e)) 
        print "ajax_delete_answer except !"
        data = {
        'result': 'false'
        }
 
    return JsonResponse(data)    
    
def ajax_update_answer(request):
    answer_pk = request.GET.get('answer_pk',None)
    new_answer_content = request.GET.get('new_answer_content',None)

    new_answer_content = new_answer_content.encode('UTF-8')
    # print "answer_pk = {} + content = {}".format(answer_pk,new_answer_content)
    

    try:
        answer = Answer.objects.get(pk=answer_pk)
        answer.answer = new_answer_content
        answer.save()
        print "answer updated {}".format(answer.answer)
        data = {
        'result': 'true',
        'updated_answer_pk' : answer_pk,
        'updated_answer' : answer.answer
        }

    except Exception as e:
        print '%s (%s)' % (e.message, type(e)) 
        print "ajax_update_answer except !"
        data = {
        'result': 'false'
        }
 
    return JsonResponse(data)    
