from django.contrib import admin

from models import Question,Answer,Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'
    

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Feedback, FeedbackAdmin)
