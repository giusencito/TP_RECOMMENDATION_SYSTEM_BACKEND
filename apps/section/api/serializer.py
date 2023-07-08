from rest_framework import serializers
from apps.section.models import Section

class SectionSerializer(serializers.ModelSerializer):
    def to_representation(self,instance):
            return {
                'id': instance.id,
                'sectionname': instance.sectionname, 
                'totalscore': instance.totalscore, 
                'test': f'{instance.test.testname}'
            }
    def validate_test(self, value):
        if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar un test.")
        return value
    def validate(self, data):
        if 'test' not in data.keys():
            raise serializers.ValidationError({
                "test": "Debe ingresar un test"
            })
        return data
    class Meta:
        model = Section
        exclude = ('state','created_date','modified_date','deleted_date')