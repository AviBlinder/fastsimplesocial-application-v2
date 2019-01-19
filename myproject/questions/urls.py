from django.conf.urls import url

from . import views,views_ajax

from django.views.i18n import JavaScriptCatalog

app_name='questions'

urlpatterns = [

    # url(r"pie/$", views.question_statistics_new, name="pie"),

    url(r"new/$", views.create_question, name="create"),
    url(r"dynamic_create/$", views.dynamic_question, name="dynamic_create"),
    url(r"vote/(?P<pk>\d+)/$",views.question_voting,name="vote"),
    url(r"new/answer/$", views.CreateAnswer.as_view(), name="create_answer"),   
    url(r"new/answer_question/(?P<pk>\d+)/$", views.create_answer, name="create_answer_question"),   

    url(r"voted_by/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$",
    views.MyVotedyQuestionsList.as_view(),name="user_voted_questions"),

    url(r"by/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$",views.QuestionList.as_view(),name="logged_user_questions"),

    url(r"by/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<pk>\d+)/$",views.QuestionDetail.as_view(),name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeleteQuestion.as_view(),name="delete"),
    url(r"delete/answer/(?P<pk>\d+)/$",views.DeleteAnswer.as_view(),name="delete_answer"),    
    url(r"update/answer/(?P<pk>\d+)/$",views.UpdateAnswer.as_view(),name="update_answer"),        
    url(r"update/answer/ready/(?P<pk>\d+)/$",views.update_answer_done,name="question_editing_done"),    
    url(r"update/answer/params/(?P<pk>\d+)/$",views.update_question_params,name="update_question_params"),    
    url(r"search/$",views.SearchUserQuestions.as_view(),name="search_question"),

#AJAX views:    
    url(r'get_question_date_time/$',views_ajax.ajax_get_question_datetime,name='get_question_date_time'),
    url(r'ajax_get_question_min_answerers/$',views_ajax.ajax_get_question_min_answerers,
                                                            name='ajax_get_question_min_answerers'),
    url(r'ajax_create_answer/$',views_ajax.ajax_create_answer,name="ajax_create_answer"),
    url(r'ajax_delete_answer/$',views_ajax.ajax_delete_answer,name="ajax_delete_answer"),
    url(r'ajax_update_answer/$',views_ajax.ajax_update_answer,name="ajax_update_answer"),

#
    url(r"^$", views.QuestionList.as_view(), name="all"),

]


