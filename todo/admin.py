from django.contrib import admin
from .models import Invite

class InviteAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Invite, InviteAdmin)