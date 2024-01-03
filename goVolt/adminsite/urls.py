from django.urls import path
from . import views

urlpatterns = [
    path('users',views.admin_users_view,name='admin-users-view'),
    path('users/edit/',views.admin_edit_user_view,name='edit-user'),
    path('save_user_data', views.save_user_data, name='save_user_data'),   
    path('messages',views.admin_messages_view,name='admin-messages-view'),
    path('chats',views.admin_chats_view,name='admin-chats-view'),
    path('chargers',views.admin_chargers_view,name='admin-chats-view')
]