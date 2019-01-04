from django import forms

from models import Question,Answer

from crispy_forms.helper import FormHelper


class QuestionForm(forms.ModelForm):

    class Meta:
        fields = ("question", "group","question_picture")
        model = Question
        
class AnswerForm_old(forms.ModelForm):
    question = forms.TextInput()
    class Meta:
        model = Answer
        fields = ('question','answer',)

class AnswerForm(forms.Form):
    question = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    answer = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))

class QuestionAnswersForm(forms.Form):
    question = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True})
)
    answer = forms.CharField(required=False)
    question_picture = forms.ImageField(required=False)
    
class VoteForm(forms.Form):
    print "inside VoteForm "
#    postal_code = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),required=False)
    vote = forms.ChoiceField(       
        required=True,
        widget=forms.RadioSelect,
#        choices=CHOICES,
        )    

    
    def __init__(self,  *args, **kwargs):
        print "inside __init__ of VoteForm"
        super(VoteForm, self).__init__(*args, **kwargs)
        initial_arguments = kwargs.get('initial', None)
        if initial_arguments:
            answer_choices = initial_arguments.get('answer_list',None)
            answer_choices = tuple(answer_choices)
            print "answer_list = {}".format(answer_choices)
#            self.fields['vote'].choices = answer_choices
            self.fields['vote'] = forms.ChoiceField(
            choices=answer_choices ,widget=forms.RadioSelect)
        else:
            print "no initial arguments!! {}"