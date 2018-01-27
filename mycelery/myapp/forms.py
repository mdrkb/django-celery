from django import forms
from django.core.validators import MinValueValidator


class GenerateRandomUserForm(forms.Form):
    total_user = forms.IntegerField(
        label='Number of users',
        required=True,
        validators=[
            MinValueValidator(10)
        ]
    )
