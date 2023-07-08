from rest_framework import serializers
from apps.question.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    def to_representation(self,instance):
            return {
                'id': instance.id,
                'questionname': instance.questionname, 
                'section': f'{instance.section.sectionname}'
            }
    def validate_section(self, value):
        if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una pregunta.")
        return value
    def validate(self, data):
        if 'section' not in data.keys():
            raise serializers.ValidationError({
                "pregunta": "Debe ingresar un pregunta"
            })
        return data
    class Meta:
        model = Question
        exclude = ('state','created_date','modified_date','deleted_date')