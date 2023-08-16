from rest_framework import serializers
from apps.resultTest.models import ResultTest


class ResultTestSerializer(serializers.ModelSerializer):
    
        def to_representation(self,instance):
            return{
                'id':instance.id,
                'obtainDate': instance.obtainDate,
                'postulant': f'{instance.postulant.username}'
            }
        def validate_postulant(self, value):
            if value == '' or value == None:
                raise serializers.ValidationError("Debe ingresar una postulant.")
            return value
        def validate(self, data):
            if 'postulant' not in data.keys():
                raise serializers.ValidationError({
                "postulant": "Debe ingresar un postulant"
            })
            return data
        class Meta:
            model = ResultTest
            exclude = ('state','created_date','modified_date','deleted_date')