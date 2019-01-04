from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.urls import reverse,reverse_lazy
from django.db import IntegrityError
from django.shortcuts import render , get_object_or_404 , redirect

from django.views.generic import DetailView,ListView,CreateView,UpdateView,RedirectView
from groups.models import Group,GroupMember
from . import models

class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ("name", "description")
    model = Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group


class JoinGroup(CreateView):
    model = Group
    fields = ['name','description']
    pk_url_kwarg = 'slug'
    template_name = 'group_form.html'
    success_url = reverse_lazy("groups:single")
    

    def form_valid(self, form,slug):
        group = form.save(commit=False)
        GroupMember.objects.create(member=self.request.user,group=group)
        group.save()

        return redirect('groups:single',slug=slug)



class LeaveGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super(LeaveGroup,self).get(request, *args, **kwargs)