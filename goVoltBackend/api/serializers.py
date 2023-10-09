from rest_framework import serializers
from api.models import Producto, Client, Venta, VentaProducto, Person
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ('created_at',)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'
        extra_kwargs = {
            'fecha': {'read_only': True, 'required': False},
            # 'fecha': {'read_only': True},
        }        
class VentaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaProducto
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email']
         #esconder password
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user