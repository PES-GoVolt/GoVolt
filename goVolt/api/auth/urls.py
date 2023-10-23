from django.urls import path
from .views import LoginApiView, LogOutApiView, RegisterApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogOutApiView.as_view(), name='logout'),
    path('register/', RegisterApiView.as_view(), name='register'),
]