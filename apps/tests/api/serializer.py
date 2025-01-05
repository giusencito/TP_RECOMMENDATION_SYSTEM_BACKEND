from rest_framework import serializers
from apps.tests.models import Test
from apps.option.models import Option
from apps.question.models import Question
from apps.section.models import Section
class TestSerializer(serializers.ModelSerializer):
    def to_representation(self,instance):
            return {
                'id': instance.id,
                'testname': instance.testname, 
                'testdescription': instance.testdescription, 
                'typetest': f'{instance.typetest.typename}'
            }
    def validate_typetest(self, value):
        if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un typetest.")
        return value
    def validate(self, data):
        if 'typetest' not in data.keys():
            raise serializers.ValidationError({
                "typetest": "Debe ingresar un typetest"
            })
        return data
    class Meta:
        model = Test
        exclude = ('state','created_date','modified_date','deleted_date')
        
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'optionname', 'optionscore']    
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True, source='option_set')  
    class Meta:
        model = Question
        fields = ['id', 'questionname', 'options']
class SectionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')  
    class Meta:
        model = Section
        fields = ['id', 'sectionname', 'totalscore', 'questions']
class TestGeneralSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True, source='section_set') 
    class Meta:
        model = Test
        fields = ['id', 'testname', 'testdescription', 'typetest', 'sections']
       
        
