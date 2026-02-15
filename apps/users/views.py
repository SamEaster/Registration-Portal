from competitions.models import Module
from django.utils.html import strip_tags
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import message, send_mail, BadHeaderError
from django.http import HttpResponse
from django.views import View
from .utils import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm,UserRegister2Form
from django.core.mail import send_mail
from .models import NewUser
from django.urls import reverse
from django.conf import settings
import requests
import secrets
import random  # Add this line at the top
from datetime import timedelta
from django.contrib.sites.models import Site
from django.utils import timezone
from django.shortcuts import get_object_or_404



User = get_user_model()

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}. It is valid for 5 minutes."
    print(otp)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])

def verify_otp(request, user_id):
    # Step 1: Retrieve the user instance
    user = get_object_or_404(NewUser, id=user_id)
    print(user)
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        # Ensure OTP and its creation time are checked from the user instance
        stored_otp = user.otp1
        otp_created_at = user.otp_created_at
        
        # Validate OTP and time limit
        if stored_otp and otp_created_at:
            if entered_otp == stored_otp and timezone.now() < otp_created_at + timedelta(minutes=5):
                # OTP is valid; activate the user
                user.is_active = True
                user.save()
                
                # Clear OTP data for security
                user.otp1 = None
                user.otp_created_at = None
                user.save()
                
                messages.success(request, "Registration successful!")
                return redirect('teaminfo',user_id = user.id )
            else:
                messages.error(request, "Invalid or expired OTP.")
    
    return render(request, 'authentication/verify_otp.html',{"email":user.email})

########### register here #####################################

def registeration_success(request):
    return render(request,'authentication/registeration_success.html') 

def registeration_failure(request):
    return render(request,'authentication/registeration_failure.html')

    







from django.db import transaction

@transaction.atomic

def register(request):
    # print(domain)
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            error_messages = {}
            for field, errors in form.errors.items():
                error_messages[field] = [str(error) for error in errors]
            messages.error(request, 'Invalid Email or Password. Kindly fill the form properly.')
            return render(
                request, 
                'authentication/register.html', 
                {'form': form, 'title': 'Register Here', 'active_page': 'signup'}
            )
        if form.is_valid():
            unique_username = form.cleaned_data['fullname']
            print(unique_username)
            if request.POST.get('referred_by'):
                alcherid = request.POST.get('referred_by')
                requests.put('https://ambassador.alcheringa.in/api/referal_id/', data={'alcherid': alcherid, 'points': 50})

            user = form.save(commit=False)
            user.username = unique_username
            user.is_active = False  # User remains inactive until OTP verification
            user.generate_otp()  # Generates and saves an OTP with the current timestamp
            user.save()
            
            # Create team member and team
           

            # Send OTP email for verification
            send_otp_email(user.email, user.otp1)
            messages.success(request, 'An OTP has been sent to your email for verification.')

            # Redirect to OTP verification page with the user's ID
            return redirect('verify_otp', user_id=user.id)

        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    else:
        form = UserRegisterForm()

    return render(request, 'authentication/register.html', {'form': form, 'title': 'Register Here', 'active_page': 'signup'})

def teaminfo(request, user_id):
    user = NewUser.objects.filter(id=user_id).first()  # Fetch the user from the database
    if not user:
        # Handle case if user does not exist
        return redirect('login')  # Redirect or show an error

    if request.method == 'POST':
        form = UserRegister2Form(request.POST)
        if not form.is_valid():
            error_messages = {}
            for field, errors in form.errors.items():
                error_messages[field] = [str(error) for error in errors]
            messages.error(request, 'Invalid Email or Password. Kindly fill the form properly.')
            return render(
                request, 
                'authentication/register.html', 
                {'form': form, 'title': 'Register Here', 'active_page': 'signup'})
        if form.is_valid():
            # Get data from the form
            teamname = form.cleaned_data['teamname']
            collegename = form.cleaned_data['collegename']
            city = form.cleaned_data.get('city', '')
            state = form.cleaned_data.get('state', '')

            # Update the user model
            user.collegename = collegename
            user.city = city
            user.state = state
            user.save()

            # Create a TeamMembers instance
            memberid = create_new_ref_number()
            member = TeamMembers(
                memberid=memberid,
                name=user.fullname,
                email=user.email,
                phone=user.phone_number,
                gender=user.gender,
            )
            member.save()

            # Create a Team instance
            team = Team(name=teamname, leader=user)
            team.save()
            team.members.add(member)
            team.save()

            # Redirect to login or success page
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegister2Form()

    return render(request, 'authentication/register_2.html', {
        'user_id':user.id,
        'form': form,
        'title': 'Register Here',
        'active_page': 'signup',
    })



def send_email_verification(request, user):
    subject = 'Activate Your Account'
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = Site.objects.get_current()

    domain = request.META['HTTP_HOST']
    link = reverse('verify_email', kwargs={
                    'uidb64': uidb64, 'token': token_generator.make_token(user)})
    message = render_to_string('authentication/email_verify_mail copy.txt', {
        'user': user,
        "link": 'https://'+domain+link,
    })
    user_email=user.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [
                user_email], fail_silently=False)

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
       
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'authentication/registeration_success.html')
        else:
            return render(request, 'authentication/registeration_failure.html')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'authentication/registeration_failure.html')

################ login forms###################################################

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        user = NewUser.objects.filter(email=email).first()
        if user:
            # if user.is_active == False:
            #     messages.error(request, "Account not verified")
               
            # else:
                      
                user = authenticate(request, email=email, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect(request.GET.get('next', 'home'))
                else:
                    print("errrr")
                    messages.error(
                        request, 'Password is incorrect for the email address entered ')
        else:
            print("email not registered")
            messages.error(request, 'Email is not registered')

    return render(request, 'authentication/login.html', {'title': 'log in','active_page':"Login"})








def password_reset_request(request):
    User = get_user_model()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(
                Q(email=data, provider="email"))
            if associated_users.exists():
                associated_users.generate_otp()
                
    return render(request=request, template_name="authentication/password/password_reset.html", context={"password_reset_form": password_reset_form})

def password_reset_done(request):
    return render(request,'authentication/password/password_reset_done.html')




@login_required(login_url='login')
def profile(request):
    modules = Module.objects.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
        print(u_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'authentication/profile.html', {'heading': 'Profile', 'form': u_form, 'modules': modules, 'totalmodules': modules.count(),'active_page':'profile'})


@login_required(login_url='login')
def profileset(request):
    modules = Module.objects.all()
    user = NewUser.objects.filter(email = request.user).first()
    if user and user.phone_number:
        return redirect('home')
    

    if request.method == 'POST':
        u_form = UserUpdateForm(

            request.POST, request.FILES, instance=request.user)
        if not u_form.is_valid():
            error_messages = {}
            for field, errors in u_form.errors.items():
                error_messages[field] = [str(error) for error in errors]
            messages.error(request, 'Invalid Email or Password. Kindly fill the form properly.')
            return render(request, 'authentication/Profileset.html', {'heading': 'Profile', 'form': u_form, 'modules': modules, 'totalmodules': modules.count(),'active_page':'profile'})
        if u_form.is_valid():
            u_form.save()
            print(u_form.cleaned_data['teamname'])
            teamname = u_form.cleaned_data['teamname']
           
            messages.success(request, f'Your Profile has been Set Up!')
            # if TeamMembers.objects.filter(email = user.email).first() is None:
            memberid = create_new_ref_number()
            member = TeamMembers(memberid=memberid, name=user.fullname, email=user.email, phone=user.phone_number, gender=user.gender)
            member.save()

            team = Team.objects.filter(name=teamname, leader=user).first()
            if not team:
                team = Team(name=teamname,leader=user)
                print("new team created")
                team.save()
                team.members.add(member)
                team.save()
            else:
                team.save()
                team.members.add(member)
                team.save()
            return redirect('home')
        else:
            print(u_form.errors)  
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'authentication/Profileset.html', {'heading': 'Profile', 'form': u_form, 'modules': modules, 'totalmodules': modules.count(),'active_page':'profile'})


@login_required(login_url='login')
def profileedit(request):
    modules = Module.objects.all()
    user = NewUser.objects.filter(email = request.user).first() 
    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Profile has been updated!')
            if Team.objects.filter(leader=user).first() is None:

               memberid = create_new_ref_number()
               member=TeamMembers(memberid = memberid, name=user.fullname,email=user.email,phone=user.phone_number,gender=user.gender)
               print(member)
               member.save()
               print(Team(name="undefined", leader=user))
               team = Team(name="undefined", leader=user)
               print(team) 
               team.save() 
               team.members.add(member)   
               return redirect('profile')
            else:
                print(u_form.errors)
        print(u_form.errors)
        return redirect('profile')
 
    else:
        u_form = UserUpdateForm(instance=request.user,initial={'alternate_phone': user.alternate_phone})
        print(u_form['alternate_phone'].value())
    return render(request, 'authentication/profile_edit.html', {'heading': 'Profile', 'form': u_form, 'modules': modules, 'totalmodules': modules.count(),'active_page':'profile','alternate_phone':user.alternate_phone})


def logout(request):
    django_logout(request)
    return redirect('home')


class VerificationView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            print("err")
            return redirect('home')

def data_registered_users(request):
    users=NewUser.objects.all()
    if request.user.is_staff:
        return render(request,'authentication/registered_users.html',{'users':users})
    
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import MemberForm
from .models import TeamMembers, Team
from competitions.models import Competition
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string


def create_new_ref_number():
    memberid = "MEM-"
    memberid += str(TeamMembers.objects.count()+5001)+"-"
    memberid += get_random_string(length=4)
    if TeamMembers.objects.filter(memberid=memberid).exists():
        return create_new_ref_number()
    return memberid


@login_required(login_url='login')
def add_member(request,pk):
    memberemail = TeamMembers.objects.filter(
        email=request.POST.get('addemail'))
    if request.method == 'POST':
        if (memberemail.count() > 0):
            return HttpResponse('User with same email already exist')
        
        memberid = create_new_ref_number()
        TeamMembers(memberid = memberid, name=request.POST.get('addname'),
                    email=request.POST.get('addemail'), phone=request.POST.get('addphone'), gender=request.POST.get('addgender')).save()
            
        team = Team.objects.get(leader=request.user)
        team.members.add(TeamMembers.objects.get(
            email=request.POST.get('addemail')))
        team.save()
        if pk!='0':
            comp = Competition.objects.get(id=pk)
            team_members = team.members.all().count()
            if(team_members<comp.min_members):
                if(comp.min_members-team_members==1):
                    messages.info(request,"Add atleast " +str(comp.min_members-team_members)+ " more member to register for "+ comp.event_name)
                else:
                    messages.info(request,"Add atleast " +str(comp.min_members-team_members)+ " more members to register for "+ comp.event_name)
    return redirect('TeamMembers')


@login_required(login_url='login')
def update_member(request):
    memberemail = TeamMembers.objects.filter(email=request.POST.get('editemail'))
    member = TeamMembers.objects.get(id=request.POST.get('editid'))
    if request.method == 'POST':
        if (memberemail.count() > 0 and member not in memberemail):
            return HttpResponse('User with same email already exist')

        if(request.FILES.getlist('editimg')):
            member.img = request.FILES.getlist('editimg')[0]
        member.name = request.POST.get('editname')
        member.email = request.POST.get('editemail')
        member.phone = request.POST.get('editphone')
        member.gender = request.POST.get('editgender')
        member.save()
    return HttpResponse('OK')


@login_required(login_url='login')
def remove_member(request):
    if request.POST["id"]:
        member = TeamMembers.objects.filter(id=request.POST["id"]).first()
        team=Team.objects.get(leader=request.user)
        team.members.remove(member)
        team.save()
        member.delete()
        return HttpResponse("ok")

