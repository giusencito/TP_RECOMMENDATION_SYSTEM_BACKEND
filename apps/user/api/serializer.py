from rest_framework import  serializers 
from apps.user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timedelta
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
         model = User
         fields = ('username', 'email', 'name', 'last_name')
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    def to_representation(self, instance):
            return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email']
        }
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['iat'] = datetime.now()
        token['user'] = user.username
        token['roles'] = user.role

        return token