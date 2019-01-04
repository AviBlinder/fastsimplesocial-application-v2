from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import HttpResponse
from django.template.loader import render_to_string

from django.http import JsonResponse

from django.urls import reverse_lazy,reverse
from django.shortcuts import  get_object_or_404 , redirect , render  

from django.http import Http404
from django.views.generic import ListView,DetailView,DeleteView,UpdateView,CreateView

from braces.views import SelectRelatedMixin

import json

from django.contrib.postgres.search import SearchQuery

from . import forms
from models import Question,Answer,AnswerByUser,QuestionVotedByUser

from datetime import datetime
from django.utils.dateparse import parse_time,parse_datetime


from django.contrib.auth import get_user_model
User = get_user_model()

import sys
import re
import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
################################################################################################################
@method_decorator(login_required, name='dispatch')
class QuestionList(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = "questions/question_list.html"

    def get_queryset(self):
        try:
            # self.question_user = User.objects.prefetch_related("questions").get(username__iexact=self.request.user)

            self.questions = Question.objects.filter(user__email= self.request.user)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.questions

################################################################################################################
@method_decorator(login_required, name='dispatch')
class UserQuestions(ListView):
    model = Question
    template_name = "questions/question_list.html"

    def get_queryset(self):
        sent_username = self.kwargs.get("username")
        # print "self.kwargs.get('username') = {} ".format(sent_username)

        try:
#            self.question_user = User.objects.prefetch_related("questions").get(email=self.kwargs.get("username")
            self.question_user = Question.objects.filter(user__email= self.kwargs.get("username")

            )
        except User.DoesNotExist:
            raise Http404
        else:
#            return self.question_user.questions.all()
            return self.question_user.all()

    def get_context_data(self, **kwargs):
        context = super(UserQuestions,self).get_context_data(**kwargs)
        context["question_user"] = self.question_user
#        context["questions"] = self.question_user.questions.all()
        context["questions"] = self.question_user.all()

        return context
################################################################################################################
@method_decorator(login_required, name='dispatch')
class MyQuestionsList(ListView):
    model = Question
    template_name = "questions/question_list.html"

    def dispatch(self, *args, **kwargs):
        self.username = kwargs['username']
        return super(MyQuestionsList, self).dispatch(*args, **kwargs)

    

    def get_queryset(self):
        sent_username = self.kwargs.get("username")
        # print "self.kwargs.get('username') = {} ".format(sent_username)

        try:
            self.question_user = User.objects.prefetch_related("questions").get(username__iexact=self.username)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.question_user.questions.all()

    def get_context_data(self, **kwargs):
        context = super(MyQuestionsList,self).get_context_data(**kwargs)
        context["question_user"] = self.question_user
        context["questions"] = self.question_user.questions.all()
        return context

################################################################################################################
@method_decorator(login_required, name='dispatch')
class SearchUserQuestions(ListView):
    model = Question
    pk_url_kwarg = 'search_words'
    template_name = "questions/question_list.html"

    def get_queryset(self):
        try:
            self.question_user = Question.objects.filter(question__search=self.request.GET.get('search_question'))
#                                        user=self.request.user)
        
        except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "SearchUserQuestions except !"
 
#            raise Http404
        else:
            return self.question_user

    def get_context_data(self, **kwargs):
        context = super(SearchUserQuestions,self).get_context_data(**kwargs)
        context["questions"] = self.question_user
        return context


###########################################################################################################
@method_decorator(login_required, name='dispatch')
class QuestionDetail( SelectRelatedMixin,DetailView):
    model = Question
    select_related = ["user"]
    pk_url_kwarg = 'pk'
    form_class = forms.QuestionForm


    def get_queryset(self):
        queryset = super(QuestionDetail,self).get_queryset()
        return queryset.filter(
            user__email =self.kwargs.get("username")
        )

    
    def get_context_data(self, **kwargs):
        context = super(QuestionDetail,self).get_context_data(**kwargs)
        chart_data , resulst_list = question_statistics(self.kwargs.get('pk'))

        # username = self.kwargs.get('username')
        # print "username = {}".format(username)
        # print "self.request.user = {}".format(self.request.user)

        context["chart"] = chart_data['chart']
        context['resulst_list'] = resulst_list
        context['form'] = forms.QuestionForm
        question_answered_by_user = QuestionVotedByUser.objects.filter(question__pk =self.kwargs.get('pk'),
                                    user__email = self.request.user).exists()
        # print "question_answered_by_user = {}".format(question_answered_by_user)                                                    
        context["question_answered_by_user"] = question_answered_by_user
        context["current_tz"] = timezone.now()
        return context

###########################################################################################################
@method_decorator(login_required, name='dispatch')
class CreateQuestion(CreateView):
    form_class = forms.QuestionForm
    model = Question

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        # image_file = self.request.FILES['question_picture']
        # print "image_file = {} ".format(image_file)
        # self.object.question_picture.save(image_file.name, image_file)
        
        self.object.save()
        return super(CreateQuestion,self).form_valid(form)
###########################################################################################################
@method_decorator(login_required, name='dispatch')
class DeleteQuestion(SelectRelatedMixin,DeleteView):
    model = Question
    select_related = ("user", "group")
#    success_url = reverse_lazy("questions:for_user")

    def get_queryset(self):
        queryset = super(DeleteQuestion,self).get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_success_url(self):
            return reverse('questions:for_user', kwargs={ 'username': self.request.user})
        

@method_decorator(login_required, name='dispatch')
class DeleteAnswer(DeleteView):
    model = Answer

    def get_success_url(self):
            answer = get_object_or_404(Answer,pk=self.kwargs.get('pk'))
            question = get_object_or_404(Question,question=answer.question)            
            return reverse('questions:single', kwargs={'pk': question.pk, 'username': question.user})

###########################################################################################################            
@method_decorator(login_required, name='dispatch')
class UpdateAnswer(UpdateView):
    model = Answer
#    form_class = forms.UpdateAnswer
    fields = ('answer',)
    template_name = 'questions/update_answer.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'answer'

    def get_success_url(self):
            answer = get_object_or_404(Answer,pk=self.kwargs.get('pk'))
            question = get_object_or_404(Question,question=answer.question)            
            return reverse('questions:single', kwargs={'pk': question.pk, 'username': question.user})
###########################################################################################################
@method_decorator(login_required, name='dispatch')
class CreateAnswer(CreateView):
    form_class = forms.AnswerForm
    model = Answer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print "pk={}".format(pk)
        question = Question.objects.get(pk=pk).question
        print "question = {}".format(question)
        return super(CreateAnswer,self).get(request, *args, **kwargs)

    def get_success_url(self):
            print "answer_pk (1) = {}".format(self.kwargs.get('pk') )
            kwargs = super(CreateAnswer,self).get_form_kwargs()
            question_pk = kwargs['data']['question']            
            username = Question.objects.get(pk=question_pk).user
            return reverse('questions:single', kwargs={'pk': question_pk, 'username': username})

####################################################################################################
@login_required
def create_question(request):

    if request.method == 'POST':
        form = forms.QuestionAnswersForm(request.POST,request.FILES)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            question_picture = request.FILES.get('question_picture', False)

            try:
                if question_picture:
                    new_question = Question(question=question,user = request.user,question_picture=question_picture)
                else:
                    new_question = Question(question=question,user = request.user)
                    
                new_question.save()
                new_answer = Answer(question=new_question,answer = answer)                
                new_answer.save()

                return redirect('questions:single', pk=new_question.pk,username = new_question.user)
                
            except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "create_question except ! (create_question)"
                messages.warning(request,("Warning, answer {} already exists".format(question)))

            else:
                print "success"
                messages.success(request,"question {question} added.".format(
                                                                question=new_question.question))
            return redirect('questions:all')
                                                               
    else:
        
        form = forms.QuestionAnswersForm()

    return render(request, 'questions/question_form.html', {'form': form})    
####################################################################################################
@login_required
def create_answer(request, pk):
    try:
        question = get_object_or_404(Question, pk=pk)
    except  question.DoesNotExist:
        raise Http404("question does not exist.")    
        
    question_answers = question.answers.all()
    answer_tuple = tuple()
    answer_list = list()
    for answer in question_answers:
        answer_list.append((answer.pk,answer.answer))     
    answer_tuple = tuple(answer_list)    

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST,request.FILES)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            try:
                Answer.objects.create(question=question,answer = answer)
            except :
                messages.warning(request,("Warning, answer {} already exists".format(answer)))

            else:
                messages.success(request,"{answer} added to question {question}.".format(answer=answer,
                                                                question=question.question))
            return redirect('questions:single', pk=question.pk,username = question.user)
            
    else:
        
        form = forms.AnswerForm(initial={'question': question.question,'question_pk' : question.pk,'answer_tuple':answer_tuple})

    return render(request, 'questions/answer_form.html', {'form': form})    
################################################################################################################################
@login_required
def question_voting(request, pk):
    
    try:
        question = get_object_or_404(Question, pk=pk)
    except  question.DoesNotExist:
        raise Http404("question does not exist !")        

    voted_by_user = QuestionVotedByUser.objects.filter(user=request.user,question=question).exists()
        
    question_answers = question.answers.all()

    answer_tuple = tuple()
    answer_list = list()
    for answer in question_answers:
        a1 = (str(answer.pk),answer.answer)
        answer_tuple = tuple(a1)
        answer_list.append(answer_tuple)     
    

    if request.method == 'POST':
        form = forms.VoteForm(answer_list,request.POST)

        if form.is_valid():
            answer = form.cleaned_data['vote']

            # print "vote3 = {}".format(answer)


            if voted_by_user:
                pass
            else:
                try:
                    updated_answer = Answer.objects.get(pk=answer)
                    updated_answer.votes = Answer.objects.get(pk=answer).increase_vote() 
                    updated_answer.save()
#                    AnswerByUser.objects.create(answer=updated_answer,user=request.user)
                    AnswerByUser.objects.create(user=request.user,question=question,answer=updated_answer)
                    
                    question.answerers = question.increase_answerers()
                    question.save()
                    QuestionVotedByUser.objects.create(user=request.user,question=question)

                except Exception as e:
                    print '%s (%s)' % (e.message, type(e)) 
                    print "question_voting except !!"
                    messages.warning(request,("Warning, answer {} already exists".format(answer)))

                else:
                    messages.success(request,"{answer} added to question {question}.".format(answer=answer.encode('utf-8'),
                                                                question=question.question.encode('utf-8')))
#        return redirect('questions:single', pk=question.pk, username = question.user)
        return redirect('questions:for_user',  username = request.user)
    else:
        form = forms.VoteForm(answer_list)
        

    return render(request, 'questions/question_voting.html', 
                    {'form': form,'question': question,'voted_by_user':voted_by_user})    
#################################################################################################################
class QuestionVoteView(UpdateView):
    model = Answer
#    form_class = ItemForm
    template_name = 'questions/question_voting.html'

    def dispatch(self, *args, **kwargs):
        self.question_pk = kwargs['pk']
        return super(QuestionVoteView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        question = Question.objects.get(pk=self.pk)
        return HttpResponse(render_to_string('questions/question_voting.html', {'question': question}))
#################################################################################################################
def question_statistics(pk):

        new_list = list()
        new_dict = {}
        resulst_dict = {}
        resulst_list = list()
    
        for answer in Question.objects.get(pk=pk).answers.all().order_by('-votes'):
            new_dict = { 'name' : '{} '.format(answer.answer.encode('utf-8')) , 
                        'y' : answer.votes }
            resulst_dict = {answer.answer :   answer.votes }
            new_list.append(new_dict)
            resulst_list.append(resulst_dict)

        question_results = {  'data': new_list  }
        Options = {
                   'pie': {
            'allowPointSelect': 'true',
            'cursor': 'pointer',
            'dataLabels': {
                'enabled': 'true',
                'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
                }
            }
        }    
        chart = {
            'chart': {'type': 'pie'},
            'title': {'text': 'Results'},
            'series': [question_results],
            'plotOptions': { 'pie':{'showInLegend': 'true','allowPointSelect': 'true', 'name': ' ',
                'dataLabels':{ 'enabled':'false','format':' {point.percentage:.1f} %'}
                            }}
        }        
        dump = json.dumps(chart)
        
        home = True
        home = json.dumps((home))
        chart_data = {'chart': dump,'home': home}
        return (chart_data,resulst_list)

##############################################################################################################
def update_answer_done(request,pk):
    try:
        question = Question.objects.get(pk=pk)
        question.editing_done = True
        question.save()

    except :
        print "create_question except ! (update_answer_done)"
        messages.warning(request,("Warning, answer {} already exists".format(question.question.encode('utf8'))))
    else:
        print "success"
        messages.success(request,"question {question} added.".format(
                            question=question.question.encode('utf8')))
    return redirect('questions:single', pk=question.pk,username = question.user)
    
########################################################################################################
@login_required
def dynamic_question(request):

    if request.method == 'POST':
        post_dict = dict(request.POST.iterlists())
#        print "post_dict = {}".format(post_dict)
        if 'answer' in post_dict.keys():
            answers = post_dict['answer']
            # print "answers : {}".format(answers)
            
        form = forms.DynamicAnswerForm(request.POST or None,request.FILES or None)
    
        # for field in form:
        #     print "field: {}".format(field)
            
        if form.is_valid():
            question = form.cleaned_data['question'].encode('UTF-8')
            question = question.decode('UTF-8')
            question_picture = request.FILES.get('question_picture', False)

            print "question_picture = {}".format(question_picture)
            due_date = form.cleaned_data['due_day']
            due_time = form.cleaned_data['due_time']
            min_answerers = form.cleaned_data['minimum_answerers']
            
            # print "due_date = {}".format(due_date)
            # print "due_time = {}".format(due_time)
            # print "min_answerers = {} <> length = {}".format(min_answerers,len(min_answerers))
            
            
            def get_aware_datetime(date_str):
                ret = parse_datetime(date_str)
                if not timezone.is_aware(ret):
                    ret = timezone.make_aware(ret)
                return ret
                
            if len(due_time) == 0:
                due_time = timezone.now().time
            if len(due_date) == 0:
                due_date = timezone.now().date
            
            due_time_f = str(datetime.strptime(due_time, '%H:%M').time())
            due_date_time = due_date + ' ' + due_time_f
            parsed_datetime = get_aware_datetime (due_date_time)

            if len(min_answerers) == 0:
                min_answerers = 0

##Create question:
            try:
                new_question = Question(question=question,user = request.user)
                new_question.save()

            except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "create_question except ! (dynamic_question)"
 #               messages.warning(request,("Warning, answer {} already exists".format(question)))
                return redirect('questions:all')

            if question_picture:
                try:
                    new_question.question_picture = question_picture
                    new_question.save()
                    # data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
                # else:
                #     data = {'is_valid': False}
                except Exception as e:
                    print '%s (%s)' % (e.message, type(e)) 
                    print "question_picture except !"
 #               messages.warning(request,("Warning, answer {} already exists".format(question)))
                    return redirect('questions:all')
                 
            if min_answerers:
                try:
                    new_question.min_answerers = min_answerers
                    new_question.save()
                except Exception as e:
                    print '%s (%s)' % (e.message, type(e)) 
                    print "min_answerers except !"

            if parsed_datetime:
                try:
                    new_question.due_date = parsed_datetime
                    new_question.save()
                except Exception as e:
                    print '%s (%s)' % (e.message, type(e)) 
                    print "create_qparsed_datetimeuestion except !"


            for answer in answers:
                answer = answer.encode('UTF-8').decode('UTF-8')
#                print "answer = {}".format(answer)
                if answer != "":
                    try:
                        new_answer = Answer(question=new_question,answer = answer)                
                        new_answer.save()
                    except Exception as e:
                        print '%s (%s)' % (e.message, type(e)) 
                        print "answer insert except !"


            return redirect('questions:single', pk=new_question.pk,username = new_question.user)
        else:
            return redirect('questions:all')
    else:
        
        form = forms.DynamicAnswerForm()
        
        # for field in form:
        #     print "field: {}".format(field)
            

    return render(request, 'questions/dynamic_question.html', {'form': form})  

########################################################################################################
@login_required
def update_question_params(request,pk):

    question = Question.objects.get(pk=pk)

    if request.method == 'POST':

        form = forms.QuestionForm(request.POST,request.FILES)
    
#        print  "error in form:{}".format(form.errors)
        
        if form.is_valid():
            
            question_picture = request.FILES.get('question_picture', False)
            due_day = form.cleaned_data['due_day']
            due_time = form.cleaned_data['due_time']
            min_answerers = form.cleaned_data['min_answerers']
            answer =  form.cleaned_data['answer']
            

            print "question_picture = %s" % question_picture
            
            def get_aware_datetime(date_str):
                ret = parse_datetime(date_str)
                if not timezone.is_aware(ret):
                    ret = timezone.make_aware(ret)
                return ret

            try:
                if answer:
                    Answer.objects.create(question=question,answer=answer.encode('UTF-8'))
                    print 'answer created!'
            except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "update_question_params answer except !"
            else:
                pass
  

            try:
                if min_answerers:
                    question.min_answerers = min_answerers
                    question.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "update_question_params min_answerers except !"
            else:
                pass
            
            try:
                if due_day and due_time:
                    due_date_time = due_day + ' ' + due_time[0:5] 
                    Question.objects.filter(pk=pk).update(due_date = due_date_time)
            except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "update_question_params due_date/time except !"
            else:
                pass
                    
            try:
                if question_picture:
                    question.question_picture = question_picture
                    question.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e)) 
                print "update_question_params question_picture except !"
            else:
                pass
                    

            return redirect('questions:single', pk=question.pk,username = question.user)
    
    else:
        
        form = forms.QuestionForm(question)

        # for field in form:
        #     print "field: {}".format(field)
            

    return render(request, 'questions/question_detail.html', {'form': form,'question':question})  
    

###########################################################################################################
def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        print "selected tz = {}".format(request.session['django_timezone'])
        return redirect('/')
    else:
        return render(request, 'questions/timezones_template.html', {'timezones': pytz.common_timezones})
###########################################################################################################
def remove_session_data(request):
    prev_timezone = {}
    print "inside remove_session_data"
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        prev_timezone = request.POST['timezone']
        print "selected tz = {}".format(request.session['django_timezone'])

    for key in request.session.keys():
        print request.session[key]
#        del request.session[key]
    return render(request, 'questions/timezones_template.html', {'timezones': prev_timezone})


def jquey_samples(request):
    
    return render(request, 'questions/jquery_samples.html', {'context': "content"})

from django.contrib.auth.models import User
    
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'

    return JsonResponse(data)
    
####################################################################################################
from django.views import View
from .forms import PhotoForm

class BasicUploadView(View):
    def post(self, request):
        print "inside post"
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            print "form is valid user: {}".format(request.user)
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            print "form is not valid"
            data = {'is_valid': False}
        return JsonResponse(data)
        
######################################################################################################
def test_menu(request):
    
    content = {}
    return render(request, 'questions/test_menu.html', {'context': "content"})


######################################################################################################
# @login_required
# def AddAnswer(request, pk):
    
#     question = get_object_or_404(Question, pk=pk)
#     question_answers = question.answers.all()

#     for answer in question_answers:
#         a1 = (str(answer.pk),answer.answer)
#         answer_tuple = tuple(a1)
#         answer_list.append(answer_tuple)     
    

#     if request.method == 'POST':
#         form = forms.VoteForm(answer_list,request.POST)

#         if form.is_valid():
#             answer = form.cleaned_data['vote']

#             # print "vote3 = {}".format(answer)
            
#             try:
#                 updated_answer = Answer.objects.get(pk=answer)
#                 updated_answer.votes = Answer.objects.get(pk=answer).increase_vote() 
#                 updated_answer.save()
#                 AnswerByUser.objects.create(answer=updated_answer,user=request.user)
#                 question.answerers = question.increase_answerers()
#                 question.save()
                
#                 AnswerByUser.objects.create(user=request.user,question=question,answer=updated_answer)

#                 QuestionVotedByUser.objects.create(user=request.user,question=question,answer=updated_answer)
#             except Exception as e:
#                 print '%s (%s)' % (e.message, type(e)) 
#                 print "question_voting except !!"
#                 messages.warning(request,("Warning, answer {} already exists".format(answer)))

#             else:
#                 messages.success(request,"{answer} added to question {question}.".format(answer=answer.encode('utf-8'),
#                                                                 question=question.question.encode('utf-8')))
#             return redirect('questions:single', pk=question.pk, username = question.user)
#     else:
#         form = forms.VoteForm(answer_list)
        

#     return render(request, 'questions/question_voting.html', {'form': form,'question': question})    
