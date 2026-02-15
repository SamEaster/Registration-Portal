
from django.urls import path
from . import views
from .views import generate_invoice

urlpatterns = [
    # path('',views.home,name='registration'),
    path('search/',views.search,name='search'),
    path('eventwise_search/',views.eventwise_search,name='eventwise_search_details'),
    path('teamSearch',views.searchTeam,name="event-search"),
    path('event',views.eventRegister,name='event-register'),
    path('',views.roomAllotment,name='room-allotment'),
    path('Allotment/',views.roomAllotment,name='room-allotment'),
    path('blankets-dues/',views.blankets_dues,name='blankets_duess'),
    path('edit-blanketdues/',views.edit_blankets_dues,name='edit-blankets-duess'),
    path('submit/',views.updateData,name='updateData'),
    path('editPage/',views.editData,name='editData'),
    path('saveEdit/',views.editData,name='saveEdit'),
    path('saveEdit/submit/',views.saveEditData,name='editedDataSave'),
    path('deleteUser/<str:memid>',views.deleteUser,name='deleteUser'),
    path('general_search/',views.general_search,name="generalSearch"),
    path('all_users/',views.all_users,name="allUsers"),
    path('all_leaders/',views.all_leaders,name="leaders"),
    path('csvuploadpd',views.pdupdate),
    path('csvuploadvogue',views.vogueupdate),
    path('csvuploadrocko', views.rockoupdate),
    path('generate-invoice/', views.generate_invoice ,name="generate-invoice")
    ]
