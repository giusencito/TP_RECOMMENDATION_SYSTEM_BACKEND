from rest_framework import serializers
from apps.linkedinJobs.models import LinkedinJobs
class LinkedinJobsSerializer(serializers.ModelSerializer):
       def to_representation(self,instance):
            return {
                'id': instance.id,
                'jobName':instance.jobName,
                'jobDescription':instance.jobDescription,
                'jobUrl':instance.jobUrl,
                'jobLocation': instance.jobLocation,
                'jobCompany': instance.jobCompany,
                'jobDate': instance.jobDate,
                'posibilityPercentage':instance.posibilityPercentage,
                'resultTest': f'{instance.resultTest.id}'
                
                
                }
       def validate_resultTest(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un resultTest.")
            return value
       def validate(self, data):
            if 'resultTest' not in data.keys():
               raise serializers.ValidationError({
                "resultTest": "Debe ingresar un resultTest"
            })
            return data
        
       class Meta:
          model = LinkedinJobs
          exclude = ('state','created_date','modified_date','deleted_date')

class LinkedinJobsHistorySerializer(serializers.ModelSerializer):
       def to_representation(self,instance):
            return {
                'id': instance.id,
                'jobName':instance.jobName,
                'resultTest': f'{instance.resultTest.id}',
                'ObtainDate': f'{instance.resultTest.obtainDate}',
                
                
                }
       def validate_resultTest(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un resultTest.")
            return value
       def validate(self, data):
            if 'resultTest' not in data.keys():
               raise serializers.ValidationError({
                "resultTest": "Debe ingresar un resultTest"
            })
            return data
        
       class Meta:
          model = LinkedinJobs
          exclude = ('state','created_date','modified_date','deleted_date')