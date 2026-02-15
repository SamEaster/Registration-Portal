from django.contrib import admin
from .models import Competition,CompTeam,Module,SubmitPerformance

# Register your models here.
admin.site.register(CompTeam)
admin.site.register(Competition)
admin.site.register(Module)
admin.site.register(SubmitPerformance)
