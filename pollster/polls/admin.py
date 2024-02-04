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

# models.Poll:
    # import datetime
    # from django.contrib import admin
    # @admin.display(boolean=True, ordering="updated_at", description="Published recently?")
    # def recently_published(self):
    #     now = timezone.now().date()
    #     return now - datetime.timedelta(days=1) <= self.updated_at <= now
