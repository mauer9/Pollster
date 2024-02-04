from django.contrib import admin
from .models import Poll, Choice, Vote


# class ChoiceAdmin(admin.ModelAdmin):
#     fields = ['poll', 'text']
#
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 1
#
# class PollAdmin(admin.ModelAdmin):
#     list_display = ['text', 'pub_date', 'recently_published']
#     list_filter = ['pub_date']
#     search_fields = ['text']
#     fieldsets = [
#         ('Text information', {'fields': ['text']}),
#         ('Date information', {'fields': ['pub_date']})
#     ]
#     inlines = [ChoiceInline]
#
#
# admin.site.register(Poll, PollAdmin)
# admin.site.register(Choice, ChoiceAdmin)
