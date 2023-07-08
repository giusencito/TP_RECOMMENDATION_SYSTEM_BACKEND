from rest_framework import serializers
from apps.typetest.models import TypeTest

class TypeTestSerializer(serializers.ModelSerializer):
    def to_representation(self,instance):
            return {
                'id': instance.id,
                'typename': instance.typename,     
            }
    class Meta:
        model = TypeTest
        exclude = ('state','created_date','modified_date','deleted_date')