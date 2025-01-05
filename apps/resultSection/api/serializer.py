from rest_framework import serializers
from apps.resultSection.models import ResultSection
from apps.section.models import Section
from apps.resultTest.models import ResultTest
from apps.tests.models import Test


class ResultSectionObtainSerializer(serializers.ModelSerializer):
      def to_representation(self,instance):
            return {
                'DevelopmentPercentage': instance.developmentPercentage/100,
                'SectionId': f'{instance.section.id}',
                'ResultTest': f'{instance.resultTest.id}'
                }
      class Meta:
            model = ResultSection
            exclude = ('state','created_date','modified_date','deleted_date')
            
class ResultSectionObtainSerializer(serializers.ModelSerializer):
      def to_representation(self,instance):
            return {
                'DevelopmentPercentage': instance.developmentPercentage/100,
                'SectionId': f'{instance.section.id}',
                'ResultTest': f'{instance.resultTest.id}'
                }
      class Meta:
            model = ResultSection
            exclude = ('state','created_date','modified_date','deleted_date')

class ResultSectionSerializer(serializers.ModelSerializer):
      def to_representation(self,instance):
            return {
                'id': instance.id,
                'developmentPercentage': instance.developmentPercentage,
                'section': f'{instance.section.sectionname}',
                'test': f'{instance.section.test.testname}',
                'resultTest': f'{instance.resultTest.id}'
                }
      def validate_section(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una seccion.")
            return value
      def validate_resultTest(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una resultado del Test.")
            return value
      def validate(self, data):
            if 'section' not in data.keys():
               raise serializers.ValidationError({
                "pregunta": "Debe ingresar un pregunta"
            })
            if 'resultTest' not in data.keys():
                   raise serializers.ValidationError({
                "resultTest": "Debe ingresar un resultTest"
            })
            return data
      class Meta:
            model = ResultSection
            exclude = ('state','created_date','modified_date','deleted_date')
            
            
class ResultSectionRangeSerializer(serializers.Serializer):
    developmentPercentage = serializers.IntegerField()
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    def create(self, validated_data):
        return ResultSection.objects.create(**validated_data)   
  
  
  
  
class SectionResultSerializer(serializers.ModelSerializer):
    sectionname = serializers.CharField(source='section.sectionname')
    class Meta:
        model = ResultSection
        fields = ['sectionname', 'developmentPercentage']
class TestResultSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ['id', 'testname', 'sections']

    def get_sections(self, obj):
        result_test = self.context.get('result_test')
        sections = ResultSection.objects.filter(
            resultTest=result_test,
            section__test=obj
        )
        return SectionResultSerializer(sections, many=True).data
  
class ResultTestSerializer(serializers.ModelSerializer):
    tests = serializers.SerializerMethodField()

    class Meta:
        model = ResultTest
        fields = ['id', 'obtainDate', 'tests']

    def get_tests(self, obj):
        # Obtener todos los tests únicos relacionados con este ResultTest
        tests = Test.objects.filter(
            section__resultsection__resultTest=obj
        ).distinct()
        
        return TestResultSerializer(tests, many=True, context={'result_test': obj}).data



         
