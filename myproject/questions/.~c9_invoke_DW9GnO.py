from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from models import Question,Answer

from django.contrib.auth import get_user_model
User = get_user_model()


class QuestionList(SelectRelatedMixin, generic.ListView):
    model = Question
    select_related = ("user", "group")


class UserQuestions(generic.ListView):
    model = Question
    template_name = "questions/user_question_list.html"

    def get_queryset(self):
        try:
            self.question_user = User.objects.prefetch_related("questions").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.question_user.questions.all()

    def get_context_data(self, **kwargs):
        context = super(UserQuestions,self).get_context_data(**kwargs)
        context["question_user"] = self.question_user
        return context


class QuestionDetail(SelectRelatedMixin, generic.DetailView):
    model = Question
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super(QuestionDetail,self).get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateQuestion(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.questionForm
    fields = ('question','group')
    model = Question

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateQuestion,self).form_valid(form)


class DeleteQuestion(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Question
    select_related = ("user", "group")
    success_url = reverse_lazy("questions:all")

    def get_queryset(self):
        queryset = super(DeleteQuestion,self).get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "question Deleted")
        return super(DeleteQuestion,self).delete(*args, **kwargs)