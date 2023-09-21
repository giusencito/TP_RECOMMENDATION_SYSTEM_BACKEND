from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.option.models import Option
from apps.section.models import Section

from apps.question.models import Question
from django.http import JsonResponse
from apps.option.api.serializer import OptionSerializer
from rest_framework.decorators import action
class OptionViewSet(viewsets.ModelViewSet):
    model = Option
    serializer_class = OptionSerializer
    queryset = None
    def get_object(self, pk):
            return get_object_or_404(self.model, pk=pk)
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.get_serializer().Meta.model.objects.filter(state=True)
        return self.queryset
    def list(self, request):
        question_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "rows": question_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        section = self.get_object(pk)
        question_serializer = self.serializer_class(section)
        return Response(question_serializer.data)
     
    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'opcion eliminado correctamente'
            })
        return Response({
            'message': 'No existe la opcion que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)
    def update(self, request, pk=None):
        try:
            option = self.get_object(pk)
            serializer = self.serializer_class(option, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({'message': 'Datos inválidos', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Option.DoesNotExist:
            return Response({'message': 'La opción que intenta actualizar no existe'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def getoptionbysection(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(question_id=pk)
        questions = self.get_queryset()
        questions_serializer = self.serializer_class(questions, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": questions_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_questions_with_options(self,request, section_id):
        try:
            section = Section.objects.filter(state=True).get(pk=section_id)
            questions = Question.objects.filter(section=section,state=True)
            questions_with_options = []
            for question in questions:
                options = Option.objects.filter(question=question)
                options_data = [{'optionname': option.optionname, 'optionscore': option.optionscore} for option in options]
                question_data = {
                'questionname': question.questionname,
                'options': options_data,
                }
                questions_with_options.append(question_data)
            return JsonResponse({'sectionname':section.sectionname,'total':section.totalscore,'testname':section.test.testname,'questions': questions_with_options})
        except Section.DoesNotExist:
               return JsonResponse({'error': 'La sección no existe'}, status=404)