
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from competitions.models import Module
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumbers import PhoneNumber
from django.contrib.auth.forms import AuthenticationForm
User = get_user_model()
from .models import Teaminfo


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter Email ID*'}))
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your Full Name '}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your User Name '}),required=False)
    collegename = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your College Name '}),required=False)
    teamname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your Team Name '}), required=False)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your City '}),required=False)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your State '}),required=False)
    referred_by = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your referral code '}),required=False)            
    # teamname = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form__field', 'placeholder': 'Team Name (Keep your own name if registering solo)'}))
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='IN',attrs={'placeholder': 'Enter your Phone Number' }
    ))
    alternate_phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='IN',attrs={'placeholder': 'Enter your Phone Number' }
    ),required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form__field', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form__field', 'placeholder': 'Confirm Password'})
    )          
    

    class Meta:
        model = User
        fields = ['fullname',
                  'username',
                  'phone_number',
                  'email',
                  'collegename',
                  'city',
                  'state',
                  'referred_by',
                  'password1',
                  'password2',
                  ]
        
class UserLoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserRegister2Form(forms.ModelForm):
    collegename = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your College Name '}))
    teamname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your Team Name '}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your City '}),required=False)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your State '}),required=False)
    class Meta:
        model = Teaminfo
        fields = ['teamname',
                  'collegename',
                  'city',
                  'state',]



class UserUpdateForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='IN',attrs={'placeholder': 'Enter your Phone Number'}
    ))
    alternate_phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='IN',attrs={'placeholder': 'Enter your Phone Number' }
    ),required=False)   
    interest = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False)
    collegename = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your College Name '}))
    # teamname = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form__field', 'placeholder': 'Enter your Team Name '}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your City '}),required=False)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your State '}),required=False)
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter your Full Name '}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form__field', 'placeholder': 'Enter Email ID*'}))
    img = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['img', 'fullname',
                  'gender',
                  'phone_number',
                  'alternate_phone',
                  'email',
                  'collegename',
                  'city',
                  'state',
                
                  ]
        
class MemberForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'border-b','size':'25','placeholder':'Enter Name'}))
    phone = forms.CharField(max_length=14,widget=forms.TextInput(attrs={'class':'border-b','size':'25','placeholder':'Enter Phone Number'}))
    email = forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'border-b','size':'25','placeholder':'Enter Email'}))
    gender = forms.ChoiceField(choices=(('M','M'),('F','F')),widget=forms.Select(attrs={'class':'border-b text-gray-400 pr-36','width':'110%','placeholder':'Gender'}))