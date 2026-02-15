from django import forms
from django.forms import formset_factory
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from users.models import TeamMembers
from django.contrib.auth import get_user_model
User = get_user_model()


class AddMemberForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form__field', 'placeholder': 'Enter Email ID*'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__field', 'placeholder': 'Enter your Full Name'})
    )
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='IN',attrs={'placeholder': 'Enter Phone Number'})
    )
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form__field'}),
        initial='Male', 
    )

    class Meta:
        model = TeamMembers
        fields = ['email', 'name', 'phone_number', 'gender']

AddMemberFormSet = formset_factory(AddMemberForm,extra = 1)
