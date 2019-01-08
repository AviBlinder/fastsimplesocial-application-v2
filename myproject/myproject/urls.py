from django.conf.urls import url,include
#from django.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views

#from accounts import views as accounts_views
from questions import views as questions_views
from groups import views as groups_views
from django.views import i18n


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#Home
    url(r"^$", questions_views.QuestionList.as_view(), name="home"),

#Authentication app
#    url(r'^accounts/', include('django_warrant.urls',namespace='accounts')),

    url(r'^accounts/', include('allauth.urls')),

    url(r"^signup/", include("accounts.urls")),
    url(r"^login/", include("accounts.urls")),
    url(r"^logout/", include("accounts.urls")),
    url(r"^reset/", include("accounts.urls")),
    url(r"^settings/", include("accounts.urls")),


#Admin 
#    url(r'^admin/', admin.site.urls),
     url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
     url(r'^simple2admin/', include(admin.site.urls)),

#groups and questions apps
    url(r"^thanks/$", questions_views.QuestionList.as_view(), name="thanks"),
    url(r"^questions/", include("questions.urls", namespace="questions")),
    url(r"^groups/",include("groups.urls", namespace="groups")),    
    url(r'^feedback/$', questions_views.feedback, name='feedback'),
    url(r'^feedback_thanks/$', questions_views.feedback_thanks, name='feedback_thanks'),
    

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
