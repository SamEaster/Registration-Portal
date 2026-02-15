from django.contrib import admin
from .models import Team, TeamMembers,NewUser, Price
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'username', 'fullname',)
    list_filter = ('email',  'username', 'fullname',
                   'is_active', 'is_staff', 'id', 'alcherid', 'gender', 'is_superuser')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'fullname',
                    'is_active', 'is_staff', 'id', 'alcherid', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'collegename', 'username',
         'fullname', 'img', 'id', 'alcherid', 'city', 'team_members', 'events_registered', 'interest')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Personal', {'fields': ('about', 'phone_number', 'provider','alternate_phone')}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'collegename', 'fullname', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )

admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Team)
admin.site.register(TeamMembers)
admin.site.register(Price)