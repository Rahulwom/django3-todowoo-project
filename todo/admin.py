from django.contrib import admin
from .models import Invite

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Invite, TodoAdmin)