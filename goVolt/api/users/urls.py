from django.urls import path
from .views import LoginApiView, LogOutApiView, RegisterApiView, SeeMyProfileApiView, EditMyProfileApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogOutApiView.as_view(), name='logout'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('see-my-profile/',SeeMyProfileApiView.as_view(),name='see-my-profile'),
    path('edit-my-profile/',EditMyProfileApiView.as_view(),name='edit-my-profile')
]