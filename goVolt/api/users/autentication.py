from rest_framework.authentication import BaseAuthentication
from api.users.exceptions import NoAuthToken,InvalidAuthToken,FirebaseError
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

from firebase_admin import firestore
from rest_framework import serializers
from goVolt.settings import AUTH_DB
from goVolt.settings import FIREBASE_DB
from firebase_admin import auth
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError
import json
from rest_framework.response import Response



class FirebaseAuthentication(BaseAuthentication):
        
        def authenticate(self, request):
                
                auth_header = request.META.get("HTTP_AUTHORIZATION")
                if not auth_header:
                        raise NoAuthToken("No auth token provided")
                id_token = auth_header.split(" ").pop()
                decoded_token = None
                try:
                        decoded_token = auth.verify_id_token(id_token)
                except Exception:
                        raise InvalidAuthToken(f"Invalid auth token {id_token}")
                if not id_token or not decoded_token:
                        return None
                
                try:
                        uid = decoded_token.get("uid")
                except Exception:
                        raise FirebaseError()
                
                user, created = User.objects.get_or_create(username=uid)
                return (user, None)