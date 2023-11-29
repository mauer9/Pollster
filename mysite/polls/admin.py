from django.contrib import admin
from .models import Question, Choice


class ChoiceAdmin(admin.ModelAdmin):
    fields = ['choice_text', 'question_text', 'votes']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date', 'recently_published']
    list_filter = ['pub_date']
    search_fields = ['question_text']
    fieldsets = [
        ('Text information', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
