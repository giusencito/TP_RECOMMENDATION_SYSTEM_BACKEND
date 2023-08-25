from rest_framework import serializers
from apps.course.models import Course
class CourseSerializer(serializers.ModelSerializer):
       def to_representation(self,instance):
            return {
                'id': instance.id,
                'courseName':instance.courseName,
                'courseDescription':instance.courseDescription,
                'Url':instance.Url,
                'job': f'{instance.job.id}'
                }
       def validate_job(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un job.")
       def validate(self, data):
            if 'job' not in data.keys():
               raise serializers.ValidationError({
                "job": "Debe ingresar un job"
            })
            return data
        
       class Meta:
          model = Course
          exclude = ('state','created_date','modified_date','deleted_date')