from django.forms import ModelForm, EmailInput
from .models import Mail


class MailForm(ModelForm):
    class Meta:

        model = Mail
        fields = ['email']

        widgets = {
            "email": EmailInput(attrs={
                'placeholder': 'e-mail',
            })
        }
