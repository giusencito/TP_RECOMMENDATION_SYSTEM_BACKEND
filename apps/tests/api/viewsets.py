from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.tests.models import Test
from apps.section.models import Section
from apps.question.models import Question
from apps.option.models import Option

from apps.tests.api.serializer import TestSerializer
from rest_framework.decorators import action
class TestViewSet(viewsets.ModelViewSet):
    model = Test
    serializer_class = TestSerializer
    queryset = None
    def get_object(self, pk):
            return get_object_or_404(self.model, pk=pk)
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.get_serializer().Meta.model.objects.filter(state=True)
        return self.queryset
    def list(self, request):
        inventory_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "rows": inventory_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        inventtory = self.get_object(pk)
        inventtory_serializer = self.serializer_class(inventtory)
        return Response(inventtory_serializer.data)
    @action(detail=True, methods=['get'])
    def getTestbyTypeTest(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(typetest_id=pk)
        assitans = self.get_queryset()
        assitans_serializer = self.serializer_class(assitans, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": assitans_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'])
    def get_test_with_sections_and_questions(self, request, pk=None):
        print(pk)
        test = get_object_or_404(self.serializer_class.Meta.model, pk=pk)
        test_serializer = self.serializer_class(test)
        test_data = test_serializer.data
        sections_data = []
        sections = Section.objects.filter(test=test,state=True)
        for section in sections:
            section_data = {
                "section": section.sectionname,
                "totalscore": section.totalscore,
                "questions": []
            }
            questions = Question.objects.filter(section=section)
            for question in questions:
                question_data = {
                    "questionname": question.questionname,
                    "options": []
                }
                options = Option.objects.filter(question=question)
                for option in options:
                    option_data = {
                        "optionname": option.optionname,
                        "optionscore": option.optionscore
                    }
                    question_data["options"].append(option_data)
                section_data["questions"].append(question_data)
            sections_data.append(section_data)
            
            
        test_data["sections"] = sections_data   
        return Response(test_data, status=status.HTTP_200_OK)