from rest_framework import serializers
from apps.InterviewQuestions.models import InterviewQuestions
class InterviewQuestionSerializer(serializers.ModelSerializer):
       def to_representation(self,instance):
            return {
                'id': instance.id,
                'question':instance.question,
                'answer':instance.answer,
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
          model = InterviewQuestions
          exclude = ('state','created_date','modified_date','deleted_date')