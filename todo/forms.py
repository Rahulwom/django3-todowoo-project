from django.forms import ModelForm
from .models import Invite

class InviteForm(ModelForm):
    class Meta:
        model = Invite
        fields = ['host_name', 'address', 'important']
