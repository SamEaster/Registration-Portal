from django.db import models
from django.utils.translation import gettext as _ 


class File(models.Model):
    name1 = models.CharField(_("name1"), max_length=100)
    email1 = models.CharField(_("email1"), max_length=100)
    contact1 = models.IntegerField(_("contact1"))
    squad = models.CharField(_("squad"), max_length=20)   
    language = models.CharField(_("language"), max_length=4)
    def __str__(self):
        return self.name1