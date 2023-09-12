from rest_framework import serializers
from apps.selectedjob.models import SelectedJob
from apps.postulants.models import Postulant
class SelectedJobSerializer(serializers.ModelSerializer):
       def to_representation(self,instance):
            return {
                'id': instance.id,
                'register':instance.register,
                'job': f'{instance.job.id}'
                }
       def validate_job(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un job.")
            return value
       def validate(self, data):
            if 'job' not in data.keys():
               raise serializers.ValidationError({
                "job": "Debe ingresar un job"
            })
            return data
        
       class Meta:
          model = SelectedJob
          exclude = ('state','created_date','modified_date','deleted_date')
          
class SelectedJobEmailSerializer(serializers.ModelSerializer):
       def to_representation(self,instance):
            return {
                'id': instance.id,
                'register':instance.register,
                'jobName': f'{instance.job.jobName}'
                }
       def validate_job(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un job.")
            return value
       def validate(self, data):
            if 'job' not in data.keys():
               raise serializers.ValidationError({
                "job": "Debe ingresar un job"
            })
            return data
        
       class Meta:
          model = SelectedJob
          exclude = ('state','created_date','modified_date','deleted_date')
class SendTestReviewSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        try: 
           
            user =  Postulant.objects.filter(is_active=True).get(email=value)
            print(user)
        except Postulant.DoesNotExist:
            raise serializers.ValidationError( {'message':'correo no existe'}  )  
        print(type(user))  
        return user