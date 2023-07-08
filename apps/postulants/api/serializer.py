from rest_framework import  serializers
from apps.postulants.models import Postulant

class PostulantSerializer(serializers.ModelSerializer):
    class Meta:
        model =Postulant
        fields = '__all__'
    def create(self,validated_data):
            print('creando')
            postulant = Postulant(**validated_data)
            postulant.set_password(validated_data['password'])
            postulant.save()
            return postulant
class PostulantListSerializer(serializers.ModelSerializer):
     class Meta:
            model = Postulant
     def to_representation(self, instance):
            print(instance)
            return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email']
        }
class UpdatePostulantSerializer(serializers.ModelSerializer):
    class Meta:
         model = Postulant
         fields = ('username', 'email', 'name', 'last_name')
         
         
         
class UpdatePostulantNameSerializer(serializers.ModelSerializer):
      class Meta:
         model = Postulant
         fields = ['name']
         
         
class UpdatePostulantLastnameSerializer(serializers.ModelSerializer):
      class Meta:
         model = Postulant
         fields = ['last_name']