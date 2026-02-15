import uuid
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from email.policy import default
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_delete, pre_save
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta
import uuid
import random

def create_new_ref_number():
    alcherid = "ALC-"
    try:
        alcherid += str(NewUser.objects.count()+5001)+"-"
        alcherid += get_random_string(length=4)
        if NewUser.objects.filter(alcherid=alcherid).exists():
            return create_new_ref_number()
    except:
        alcherid += str(5001)+"-"
        alcherid += get_random_string(length=4)
    return alcherid

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,  ** other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    otp1 = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    def generate_otp(self):
        self.otp1 = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
    
    def is_otp_valid(self):
        if self.otp_created_at and timezone.now() < self.otp_created_at + timedelta(minutes=5):
            return True
        return False
    GENDER=(('M','Male'),('F','Female'),('O','Others'))
    gender=models.CharField(choices=GENDER,default='M',max_length=20)
    alcherid = models.CharField(
        max_length=255, blank=True, unique=True)
    referred_by = models.CharField(
        max_length=255, blank=True)
    otp = models.CharField(max_length=6,default='000000')     
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    img = models.ImageField(upload_to="image_uploads/userdp/",
                            default='user-default.png')
    email = models.EmailField(_('email address'), unique=True)
    
    username = models.CharField(max_length=150, unique=True,blank=True)
    collegename = models.CharField(max_length=150, unique=False)
    city = models.CharField(max_length=150, unique=False,blank=True)
    state = models.CharField(max_length= 200, unique=False,blank=True)
    fullname = models.CharField(max_length=150, )
    phone_number = PhoneNumberField(max_length = 14, unique=False, )

    alternate_phone = models.CharField(max_length = 14, unique=False, blank=True)
    interest = models.ManyToManyField(
        "competitions.Module", related_name="interest")
    # teamname = models.CharField(max_length=150, unique=False,default="")    
    team_members=models.IntegerField(default=0)
    events_registered = models.ManyToManyField(
        "competitions.Competition", related_name="competition",blank=True)

    date_joined = models.DateTimeField(default=timezone.now)
    provider = models.CharField(max_length=200, unique=False, default="email")
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.email)
    
    def save(self, *args, **kwargs):
        if not self.alcherid:
            self.alcherid = create_new_ref_number()
        return super(NewUser,self).save(*args,**kwargs)

class TeamMembers(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Others')
    ]
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    memberid = models.CharField(
        max_length=255, default="MEM-XXXX-XXXX")
    img = models.ImageField(upload_to="image_uploads/userdp/",
                            default='user-default.png')
    email = models.EmailField()
    name = models.CharField(max_length=150, blank=True)
    phone = PhoneNumberField()
    gender = models.CharField(choices = GENDER_CHOICES,max_length=1,default='M')
    accomodation = models.BooleanField(default=False, blank=True)
    daysStay = models.IntegerField(default=0)
    accomodation_type=models.CharField(default='none',max_length=14)
    
    
    def __str__(self):
        return str(self.email)
    

Accomodation_choices=[
    ('Y','Yes'),
    ('N','No')
]
    
class Team(models.Model) :
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    name=models.CharField(max_length=150,null=True)
    leader = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="team", on_delete=models.CASCADE)
    members = models.ManyToManyField(TeamMembers)
    blankets = models.IntegerField(default=0)    
    dues = models.IntegerField(default=0)
    
    Accomodation=models.CharField(choices = Accomodation_choices,max_length=1,default='N',null=True, blank=True)   
    totalPaid=models.IntegerField(default=0)

    def __str__(self):
        return str(self.leader)

class Teaminfo(models.Model):
    collegename = models.CharField(max_length=150, unique=False)
    city = models.CharField(max_length=150, unique=False,blank=True)
    state = models.CharField(max_length= 200, unique=False,blank=True)
    teamname =models.CharField(max_length=150,null=True)

class Price(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    

    


# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def create_profile_post_save(sender,instance,created,*args,**kwargs) :
#     if created:
#         if not TeamMembers.objects.filter(email=instance.email):
#             # print(instance.name,instance.fulllname,instance.username)
#             TeamMembers(email=instance.email,name=instance.fullname,phone=instance.phone, gender='M').save()
#             team=Team.objects.create(leader=instance)
#             team.members.add(TeamMembers.objects.get(email=instance.email))
#             team.save()

        
# @receiver(pre_save, sender=settings.AUTH_USER_MODEL)
# def create_profile_pre_save(sender, instance,*args, **kwargs):
#     if instance is None:
#         pass
#     else:
#         if(TeamMembers.objects.filter(email=instance.email).count()>0):
#             team=TeamMembers.objects.get(email=instance.email)
#             team.name=instance.username
#             team.phone=instance.phone
#             team.gender='M'
#             team.save()


# @receiver(m2m_changed, sender=Team.members.through)
# def team_members_changed(sender, instance, *args, **kwargs):
#     print(instance)
#     user=NewUser.objects.get(email=instance.leader.email)
#     user.team_members=instance.members.all().count()
#     user.save()


