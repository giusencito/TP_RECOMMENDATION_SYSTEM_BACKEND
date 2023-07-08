from apps.admins.models import Admin
from rest_framework import  serializers
from apps.user.models import User
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model =Admin
        fields = '__all__'
    def create(self,validated_data):
            
            
            admin = Admin(**validated_data)
            admin.set_password(validated_data['password'])
            admin.save()
            return admin
class AdminListSerializer(serializers.ModelSerializer):
     class Meta:
            model = Admin
     def to_representation(self, instance):
            return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email']
        }
class UpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
         model = Admin
         fields = ('username', 'email', 'name', 'last_name')
         
         
         
class UpdateAdminNameSerializer(serializers.ModelSerializer):
      class Meta:
         model = Admin
         fields = ['name']
         
         
class UpdateAdminLastnameSerializer(serializers.ModelSerializer):
      class Meta:
         model = Admin
         fields = ['last_name']