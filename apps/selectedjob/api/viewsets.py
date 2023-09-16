from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.selectedjob.models import SelectedJob
from apps.feedback.models import Feedback
from apps.selectedjob.api.serializer import SelectedJobSerializer,SelectedJobEmailSerializer,SendTestReviewSerializer
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
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
    @action(detail=False, methods=['get'])
    def getSelectedJobsbyLinkedinJobs(self, request,resulttest_id):
        self.serializer_class=SelectedJobEmailSerializer
        selected_jobs = SelectedJob.objects.filter(job__resultTest_id=resulttest_id, state=True)

        selected_jobs_serializer = self.serializer_class(selected_jobs, many=True)

        data = {
            "total": selected_jobs.count(),
            "rows": selected_jobs_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
 
    
    
    

class SendTestEmail(viewsets.GenericViewSet):
    serializer_class = SendTestReviewSerializer
    @action(detail=False, methods=['post']) 
    def send_email(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            print('fff')
            user = serializer.validated_data['user']
            Feedback = serializer.validated_data['feedback']
            #user.token_password = token
            #user.save()
            subject = 'Cuestionario de Verificación'
            from_email = 'xskulldragon@gmail.com'
            recipient_list= [user.email] 
            print(recipient_list)
            reset_password_link = f'http://localhost:4200/start-validation-test/{Feedback.token_link}/{user.id}'
            message = f'Hola {user.username},\n\nAqui esta el cuestionario de verificación sigue este enlace: {reset_password_link}\n\nAtentamente,\nEl equipo de tu aplicación'
            send_mail(subject, message,from_email, recipient_list,fail_silently=False)
            return Response({
                'message': 'correo enviado'
            })
        else:
            print(serializer.data)
            return Response({'message':'errror'},status= status.HTTP_400_BAD_REQUEST)