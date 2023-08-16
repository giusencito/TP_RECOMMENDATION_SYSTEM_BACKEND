from rest_framework import serializers
from apps.resultSection.models import ResultSection
class ResultSectionSerializer(serializers.ModelSerializer):
      def to_representation(self,instance):
            return {
                'id': instance.id,
                'developmentPercentage': instance.developmentPercentage,
                'section': f'{instance.section.sectionname}',
                'resultTest': f'{instance.resultTest.id}'
                }
      def validate_section(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una seccion.")
      def validate_resultTest(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una resultado del Test.")
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