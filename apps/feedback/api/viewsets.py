
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.feedback.models import Feedback
from apps.feedback.api.serializer import FeedbackSerializer,FeedbackReviewSerializer
from rest_framework.decorators import action



class FeedbackViewSets(viewsets.ModelViewSet):
    model = Feedback
    serializer_class = FeedbackSerializer
    queryset = None
    def get_object(self, pk):
            return get_object_or_404(self.model, pk=pk)
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.get_serializer().Meta.model.objects.filter(state=True)
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
                'message': 'pregunta eliminado correctamente'
            })
        return Response({
            'message': 'No existe la pregunta que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def getFeedbackbyAdmin(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(admin_id=pk)
        Feedback = self.get_queryset()
        Feedback_serializer = self.serializer_class(Feedback, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": Feedback_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'])
    def getFeedbackbyresultTest(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(resultTest_id=pk)
        Feedback = self.get_queryset()
        Feedback_serializer = self.serializer_class(Feedback, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": Feedback_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'])
    def getFeedbackbyselectedJob(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(selectedjob=pk)
        Feedback = self.get_queryset()
        Feedback_serializer = self.serializer_class(Feedback, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": Feedback_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def get_feedback_by_result_test(self, request, result_test_id):
        self.serializer_class=FeedbackReviewSerializer
        feedback = Feedback.objects.filter(selectedjob__job__resultTest__id=result_test_id, state=True)
        feedback_serializer = self.serializer_class(feedback, many=True)
        data = {
            "total": feedback.count(),
            "rows": feedback_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    