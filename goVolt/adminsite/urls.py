from django.urls import path
from . import views

urlpatterns = [
    path('users',views.admin_users_view,name='admin-users-view'),
    path('users/edit/',views.admin_edit_user_view,name='edit-user'),
    path('save_user_data', views.save_user_data, name='save_user_data'),   
    path('messages',views.admin_messages_view,name='admin-messages-view'),
    path('chats',views.admin_chats_view,name='admin-chats-view'),
    path('chargers',views.admin_chargers_view,name='admin-chargers-view'),
    path('bikestations',views.admin_bikestations_view,name='admin-bikestations-view'),
    path('routes',views.admin_routes_view,name='admin-routes-view'),
    path('delete-charger',views.charger_delete_post,name='delete-charger'),
    path('delete-route',views.route_delete_post,name='delete-route'),
    path('delete-bikestation',views.bikestation_delete_post,name='delete-bikestation')
]