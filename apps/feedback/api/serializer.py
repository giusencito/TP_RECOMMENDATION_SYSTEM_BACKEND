from rest_framework import serializers
from apps.feedback.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
      def to_representation(self,instance):
            return {
                'id': instance.id,
                'emailsend': instance.emailsend,
                'resultTest': f'{instance.resultTest.id}',
                'admin': f'{instance.admin.id}',
                'token_link': f'{instance.token_link}',
                'selectedjob': f'{instance.selectedjob.id}',
                
            }
      
      def validate_admin(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un admin.")
            return value 
      def validate_postulant(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un postulant.")
            return value
      def validate_resultTest(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un resultTest.")
            return value
      def validate_selectedjob(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un selectedjob.")
            return value
      def validate(self, data):
            
            if 'admin' not in data.keys():
                   raise serializers.ValidationError({
                "admin": "Debe ingresar un admin"
            })
            if 'resultTest' not in data.keys():
                       raise serializers.ValidationError({
                "resultTest": "Debe ingresar un postulant"
            })
            if 'selectedjob' not in data.keys():
                   raise serializers.ValidationError({
                "selectedjob": "Debe ingresar un selectedjob"
            })
            return data
            
            
            
      class Meta:
              model = Feedback
              exclude = ('state','created_date','modified_date','deleted_date')
              
              
class FeedbackReviewSerializer(serializers.ModelSerializer):
     def to_representation(self,instance):
            return {
                'id': instance.id,
                'emailsend': instance.emailsend,
                'resultTest': f'{instance.resultTest.id}',
                'admin': f'{instance.admin.id}',
                'selectedjob': f'{instance.selectedjob.job.jobName}',
                
            }
     class Meta:
              model = Feedback
              exclude = ('state','created_date','modified_date','deleted_date')