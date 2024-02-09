from django.contrib import admin
from .models import Poll, Choice, Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ["voter", "choice", "poll", "created_at", "updated_at"]
    fields = ["voter", "choice", "poll", "created_at"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["text", "poll", "created_at", "updated_at"]
    fields = ["poll", "text"]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class PollAdmin(admin.ModelAdmin):
    list_display = ["text", "created_at", "updated_at"]
    list_filter = ["created_at"]
    search_fields = ["text"]
    fieldsets = [
        ("Text information", {"fields": ["text"]}),
        ("Date information", {"fields": ["created_at"]}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
