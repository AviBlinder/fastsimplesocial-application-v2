from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm

from django.contrib.auth.decorators import login_required
##from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
#    fields = ('first_name', 'last_name', 'email', )
    fields = ( 'first_name', 'last_name', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
##################################################################################################
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.core.mail import EmailMessage

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            
            print "current_site = {}".format(current_site)

            mail_subject = 'FastSimpleSocial - Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
#            return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, 'signup_confirmation.html')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    
#######
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
#        user = User.objects.filter(pk=uid)        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        print '%s (%s)' % (e.message, type(e)) 
        print "activate except !"        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def signuptest(request):
    return render(request, 'signup_confirmation.html')
