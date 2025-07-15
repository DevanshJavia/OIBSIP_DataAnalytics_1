from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class HousePriceForm(forms.Form):
    area = forms.FloatField(label='Area (in sq ft)', min_value=0)
    bedrooms = forms.IntegerField(label='Bedrooms', min_value=0)
    bathrooms = forms.IntegerField(label='Bathrooms', min_value=0)
    stories = forms.IntegerField(label='Stories', min_value=0)
    parking = forms.IntegerField(label='Parking', min_value=0)

    mainroad = forms.ChoiceField(
        label='Main Road Access',
        choices=[('yes', 'Yes'), ('no', 'No')]
    )

    guestroom = forms.ChoiceField(
        label='Guest Room',
        choices=[('yes', 'Yes'), ('no', 'No')]
    )

    basement = forms.ChoiceField(
        label='Basement',
        choices=[('yes', 'Yes'), ('no', 'No')]
    )

    hotwaterheating = forms.ChoiceField(
        label='Hot Water Heating',
        choices=[('yes', 'Yes'), ('no', 'No')]
    )

    airconditioning = forms.ChoiceField(
        label='Air Conditioning',
        choices=[('yes', 'Yes'), ('no', 'No')]
    )

    prefarea = forms.ChoiceField(
        label='Preferred Area',
        choices=[('yes', 'Yes'), ('no', 'No')]
    )

    furnishingstatus = forms.ChoiceField(
        label='Furnishing Status',
        choices=[
            ('furnished', 'Furnished'),
            ('semi-furnished', 'Semi-Furnished'),
            ('unfurnished', 'Unfurnished')
        ]
    )

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
