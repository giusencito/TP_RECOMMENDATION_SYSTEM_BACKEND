from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.linkedinJobs.models import LinkedinJobs
from apps.linkedinJobs.api.serializer import LinkedinJobsSerializer,LinkedinJobsHistorySerializer
from rest_framework.decorators import action
from django.db.models import Subquery, F, Min,OuterRef
class LinkedinJobsViewSets(viewsets.ModelViewSet):
    model = LinkedinJobs
    serializer_class = LinkedinJobsSerializer
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
                'message': 'pregunta eliminado correctamente'
            })
        return Response({
            'message': 'No existe la pregunta que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['get'])
    def getLinkedinJobbyResultTest(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(resultTest_id=pk)
        Linkedinjob = self.get_queryset()
        Linkedinjob_serializer = self.serializer_class(Linkedinjob, many=True)
        data = {
            
            "total": self.get_queryset().count(),
            "rows": Linkedinjob_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['get'])
    def getLinkedinJobbyResultTestJustOne(self,request,pk=None):
       
        self.queryset = self.serializer_class().Meta.model.objects.filter(state=True).filter(resultTest_id=pk).first()
        Linkedinjob = self.get_queryset()
        if Linkedinjob:
           Linkedinjob_serializer = self.serializer_class(Linkedinjob)
           data = {
            "Linkedinjob": Linkedinjob_serializer.data
           }
           return Response(data, status=status.HTTP_200_OK)
        else:
             return Response({"message": "Error Match"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['get'])
    def getLinkedinJobsByResultTestAndPostulant(self, request, result_test_id, postulant_id):
        self.serializer_class=LinkedinJobsHistorySerializer
        linkedinJobs = LinkedinJobs.objects.filter(
            resultTest_id=result_test_id, state=True,resultTest__postulant_id=postulant_id
        )
        linkedinJobs_serializer = self.serializer_class(linkedinJobs, many=True)

       
        data = {
            "total": linkedinJobs.count(),
            "rows": linkedinJobs_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def getLinkedinJobsByPostulantsJustOne(self, request,postulant_id):
        self.serializer_class=LinkedinJobsHistorySerializer
        linkedinJobs = LinkedinJobs.objects.filter(
                    state=True, resultTest__postulant_id=postulant_id
                      )
        min_result_test_subquery = linkedinJobs.filter(
                       resultTest=OuterRef('resultTest')
                       ).order_by('resultTest', 'id').values('id')[:1]
        unique_linkedin_jobs = linkedinJobs.filter(id=Subquery(min_result_test_subquery))

        linkedinJobs_serializer = self.serializer_class(unique_linkedin_jobs, many=True)

       
        data = {
            "total": unique_linkedin_jobs.count(),
            "rows": linkedinJobs_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
   


    
