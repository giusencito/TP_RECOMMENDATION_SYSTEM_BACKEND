from rest_framework import serializers
from apps.selectedjob.models import SelectedJob
from apps.postulants.models import Postulant
from apps.feedback.models import Feedback
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
    token = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')

        try:
            user = Postulant.objects.get(email=email, is_active=True)
        except Postulant.DoesNotExist:
            raise serializers.ValidationError({'message': 'El correo no existe'})

        try:
            feedback = Feedback.objects.get(selectedjob__job__resultTest__postulant=user, token_link=token, state=True)
        except Feedback.DoesNotExist:
            raise serializers.ValidationError({'message': 'El feedback no existe'})

        return {'user': user, 'feedback': feedback}
    
        