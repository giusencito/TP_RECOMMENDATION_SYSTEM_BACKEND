from rest_framework import serializers
from apps.selectedjob.models import SelectedJob
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