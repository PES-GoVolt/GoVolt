from django.urls import path
from .views import RegisterApiView, SeeMyProfileApiView, EditMyProfileApiView,AchievementsApiView, ExternalUserApiView

urlpatterns = [
    path('achievement/',AchievementsApiView.as_view(),name='achievements'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('see-my-profile/',SeeMyProfileApiView.as_view(),name='see-my-profile'),
    path('edit-my-profile/',EditMyProfileApiView.as_view(),name='edit-my-profile'),
    path('external', ExternalUserApiView.as_view(), name='external-user')
]