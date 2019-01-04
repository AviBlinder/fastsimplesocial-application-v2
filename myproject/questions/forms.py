from django import forms
import datetime
#from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from models import Question,Answer,AnswerByUser

from crispy_forms.helper import FormHelper

from datetimepicker.widgets import DateTimePicker
from django.contrib.admin import widgets

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class QuestionForm(forms.ModelForm):
    
    answer = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))

    class Meta:
        fields = ("question_picture","due_day","due_time","min_answerers",)
        model = Question
        widgets = {
            'due_day':  forms.DateTimeInput(attrs={'type':'date'}),
            'due_time': forms.DateTimeInput(attrs={'type':'time'}),
            'min_answerers' : forms.TextInput(attrs={'type':'number',}),
        }
        

    def __init__(self, *args, **kwargs):

        super(QuestionForm, self).__init__(*args, **kwargs)

#        question = Question.objects.get(pk=55)
        self.fields['due_time'].required = False

        self.fields['due_day'].required = False
#        self.fields['due_day'] = question.due_day
        
        self.fields['min_answerers'].required = False
#        self.fields['min_answerers'] = question.min_answerers

        self.fields['question_picture'].required = False      
        
class AnswerForm_old(forms.ModelForm):
    question = forms.TextInput()
    class Meta:
        model = Answer
        fields = ('question','answer',)

class UpdateAnswer(forms.Form):
        answer = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))

class AnswerForm(forms.Form):
    answer = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))

class DynamicAnswerForm(forms.Form):
    
    question = forms.CharField(label='Ask a question',widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    
    answer = forms.CharField(label="your answers",required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': False}))

    question_picture = forms.FileField(required=False)

    due_day = forms.CharField(required=False,widget=forms.DateTimeInput(attrs={'type':'date'}))
    due_time = forms.CharField(required=False,widget=forms.DateTimeInput(attrs={'type':'time'}))
    
    minimum_answerers = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'number'}))                             
    
class QuestionAnswersForm(forms.Form):
    question = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
)
    answer = forms.CharField(required=False)
    question_picture = forms.ImageField(required=False)

    due_date = forms.DateField(widget=DateInput())

    
class VoteForm(forms.Form):

    def __init__(self, answer_list, *args, **kwargs):

        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['vote'].choices = answer_list

    vote = forms.ChoiceField(       
        required=True,
        widget=forms.RadioSelect
        )    
            


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_picture', )