from rest_framework import serializers
from apps.option.models import Option

class OptionSerializer(serializers.ModelSerializer):
    def to_representation(self,instance):
            return {
                'id': instance.id,
                'optionname': instance.optionname, 
                'optionscore': instance.optionscore, 
                'question': f'{instance.question.questionname}'
            }
    def validate_question(self, value):
        if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una pregunta.")
        return value
    def validate(self, data):
        if 'question' not in data.keys():
            raise serializers.ValidationError({
                "question": "Debe ingresar un question"
            })
        return data
    class Meta:
        model = Option
        exclude = ('state','created_date','modified_date','deleted_date')