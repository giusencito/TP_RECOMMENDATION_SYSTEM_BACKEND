from rest_framework import serializers
from apps.tests.models import Test

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