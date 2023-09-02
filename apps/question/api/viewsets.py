from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.question.models import Question
from apps.question.api.serializer import QuestionSerializer
from rest_framework.decorators import action
class QuestionViewSet(viewsets.ModelViewSet):
    model = Question
    serializer_class = QuestionSerializer
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
    def update(self, request, pk=None):
        try:
            question = self.get_object(pk)
            serializer = self.serializer_class(question, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({'message': 'Datos inválidos', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Question.DoesNotExist:
            return Response({'message': 'La question que intenta actualizar no existe'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'pregunta eliminado correctamente'
            })
        return Response({
            'message': 'No existe la pregunta que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['get'])
    def getquestionbySection(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(section_id=pk)
        questions = self.get_queryset()
        questions_serializer = self.serializer_class(questions, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": questions_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)