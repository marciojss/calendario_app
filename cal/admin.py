from django.contrib import admin
from cal.models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ["creator", "date", "title", "snippet"]
    list_filter = ["creator"]

admin.site.register(Entry, EntryAdmin)
