from django import forms
from channel2.account.models import User


class StaffUserAddForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        pass
