from rest_framework import serializers
from apps.feedback.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
      def to_representation(self,instance):
            return {
                'id': instance.id,
                'emailsend': instance.emailsend,
                'postulant': f'{instance.postulant.id}',
                'admin': f'{instance.admin.id}',
                'token_link': f'{instance.token_link}'
                
            }
      
      def validate_admin(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un admin.")
            return value 
      def validate_postulant(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un postulant.")
            return value
      def validate(self, data):
            
            if 'admin' not in data.keys():
                   raise serializers.ValidationError({
                "admin": "Debe ingresar un admin"
            })
            if 'postulant' not in data.keys():
                   raise serializers.ValidationError({
                "postulant": "Debe ingresar un postulant"
            })
            return data
            
            
            
      class Meta:
              model = Feedback
              exclude = ('state','created_date','modified_date','deleted_date')