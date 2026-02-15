from email.policy import default
from django.db import models
import uuid
from django.db.models.base import Model
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.conf import settings
from competitions.validators import validate_file_extension
from users.models import NewUser,TeamMembers


class Module(models.Model):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    module = models.CharField(max_length=127)
    module_query_name_without_spaces_all_small = models.CharField(
        max_length=127)
    module_icon = models.ImageField(
        upload_to="image_uploads/moduleicons/", default='module_icon_default.png')
    module_icon_active = models.ImageField(
        upload_to="image_uploads/moduleicons/active/", default='module_icon_default.png')

    def __str__(self):
        return str(self.module)



    

class Competition(models.Model):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    module = models.ForeignKey(
        Module, related_name='modulename', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_short= models.CharField(max_length=255, null=True, blank=True)
    event_tags= models.CharField(max_length=255, null=True, blank=True)
    event_desc = models.CharField(max_length=500)
    event_rules = models.TextField()
    solo_or_group = models.CharField(max_length=10,default="")
#   event_rules_pdf = models.FileField(upload_to="image_uploads/rulebooks/", validators=[validate_file_extension],  blank=True, null=True)
    min_members = models.IntegerField(default=1)
    max_members = models.IntegerField(default=1)
    prize_worth = models.CharField(max_length=255)
    online = models.BooleanField(default = True)
    image = models.ImageField(
        upload_to="image_uploads/event_pics/", default='event_default.png')
    showPeformanceLink = models.BooleanField(default=True)
    portalUrl = models.CharField(max_length=50, default='',blank=True)


    def __str__(self):
        return str(self.event_name)


class CompTeam(models.Model):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    event = models.ForeignKey(
        Competition, related_name="event_name1", on_delete=models.CASCADE)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="teams_leader", on_delete=models.CASCADE)
    team_name=models.CharField(max_length=255,default="undefined")
    members = models.ManyToManyField(TeamMembers)

    def __str__(self):
        return str(self.leader)


class SubmitPerformance(models.Model):
    event = models.ForeignKey(
        Competition, related_name="event_name2", on_delete=models.CASCADE)
    team = models.ForeignKey(
        CompTeam, related_name="compteams2", on_delete=models.CASCADE)
    link = models.CharField(max_length=2000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


# @receiver(post_save, sender=CompTeam)
# def comp_register_signal(sender, instance, created, *args, **kwargs):
#     if(created):
#         user = NewUser.objects.get(email=instance.leader.email)
#         user.events_registered.add(instance.event)
#         user.save()
