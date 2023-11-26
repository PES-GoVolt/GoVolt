from django.urls import path
from .views import RegisterApiView, SeeMyProfileApiView, EditMyProfileApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('see-my-profile/',SeeMyProfileApiView.as_view(),name='see-my-profile'),
    path('edit-my-profile/',EditMyProfileApiView.as_view(),name='edit-my-profile')
]