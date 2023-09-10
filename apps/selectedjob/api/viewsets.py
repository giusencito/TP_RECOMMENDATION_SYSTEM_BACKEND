from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.selectedjob.models import SelectedJob
from apps.selectedjob.api.serializer import SelectedJobSerializer
from rest_framework.decorators import action

class SelectedJobViewSets(viewsets.ModelViewSet):
    model = SelectedJob
    serializer_class = SelectedJobSerializer
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
                'message': 'curso eliminado correctamente'
            })
        return Response({
            'message': 'No existe el curso que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def getSelectedJobbyLinkedinJobId(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(job_id=pk)
        SelectedJob = self.get_queryset()
        SelectedJob_serializer = self.serializer_class(SelectedJob, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": SelectedJob_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)