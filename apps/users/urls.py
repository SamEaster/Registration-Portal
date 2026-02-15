
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout,name='logout'),
    path('register/', views.register, name='register'),
    path('teaminfo/<uuid:user_id>/',views.teaminfo,name ='teaminfo'),
    path('registeration_failure/',views.registeration_failure,name='registeration_failure'),
    path('registeration_success/',views.registeration_success,name='registeration_success'),
    path('profile/', views.profile, name='profile'),
    

    # path('checkotp/', views.register_user, name='register'),
    path('auth/verify-otp/<uuid:user_id>/', views.verify_otp, name='verify_otp'),

    # path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('profile_edit/', views.profileedit, name='profileedit'),
    path('profile_set/', views.profileset, name='profileset'),
    #  path('<slug:pk>/', views.team_members, name='team'),
    # path('member/add/<slug:pk>/', views.add_member, name='add-member'),
    # path('member/update', views.update_member, name='update-member'),
    # path('members/remove', views.remove_member, name='remove-member'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    # Password reset urls
    path("password_reset", views.password_reset_request, name="password_reset"),
     path("password_reset_done", views.password_reset_done, name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name="authentication/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(
        template_name='authentication/password/password_reset_complete.html'), name='password_reset_complete'),
]
