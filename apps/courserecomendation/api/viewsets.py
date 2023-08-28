from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from apps.linkedinJobs.models import LinkedinJobs
from rest_framework.decorators import action
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise.prediction_algorithms import KNNBasic
from surprise import accuracy
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import openai

class CourseRecomendationViewset(viewsets.ModelViewSet):
    todos_los_cursos = []

    def GetCourses(self):
        for pagina in range(1, 26):
            url = f'https://campusromero.pe/cursos/page/{pagina}/'
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                cursos = soup.find_all('div', class_='box-date')
                
                for curso in cursos:
                    titulo = curso.find('h3').text.strip()
                    url = curso.find_next('a')['href'] 

                    course_response = requests.get(url)
                    course_soup = BeautifulSoup(course_response.text, 'html.parser')
                    
                    course_description_box = course_soup.find('div', class_='contenido-standard')
                    
                    course_description_element = course_description_box.find('p')
                    if course_description_element is not None:
                        course_description = course_description_element.text.strip()
                    else:
                        course_description = course_description_box.find('font').text.strip()             

                    self.todos_los_cursos.append([titulo,url,course_description])
        
    @action(detail=False, methods=['get'])
    def GetAllCourses(self,request):
        self.todos_los_cursos = []
        self.GetCourses()
        coursedf = pd.DataFrame(self.todos_los_cursos,columns=['CourseTitle', 'URL', 'Description'])
        coursedf.to_csv('csv/courses.csv', sep='\t',index=False) 
        return Response(self.todos_los_cursos)
    
    
    @action(detail=True, methods=['post'])
    def CourseRecomendation(self,request,pk=None):
        job_id = pk
        print(job_id)
        
        job = get_object_or_404(LinkedinJobs, pk=job_id)
        print(type(job))
        print(job.jobName)
        print(job.jobDescription)

        cursos_solo_titulos = []
        all_courses_list = []

        course_df = pd.read_csv('csv/courses.csv',sep='\t')
        all_courses_list = course_df.to_dict(orient='records')

        cursos_solo_titulos = course_df['CourseTitle'].tolist()

        openai.api_key = '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' #verificar
        expert_tips = ['Prepararse para una buena entrevista laboral', 'Tener Experiencia','Desarrollar un buen CV', 'Tener competencias blandas', 'Tener competencias tecnicas', 'Tener valores y principios']
        prompt = [{ "role": "user",
           "content": f"Se tienen los siguientes cursos de capacitación: {cursos_solo_titulos}  Ahora te voy a pasar unos tips o consejos para conseguir un empleo de ingeniero de Software dados por un experto: {expert_tips}  Finalmente, te voy a pasar el nombre de un empleo: {job.jobName}  y su respectiva descripción: {job.jobDescription} Ahora con toda la información obtenida necesito que me recomiendes los mejores 5 cursos no tecnicos de capacitación para este empleo basándote en los nombres de los cursos que te brinde en un inicio, los tips o consejos para conseguir un empleo de ingeniero de Software dados por el experto y en la descripcion del empleo. Recuerda que los cursos que me recomiendes deben tener el enfoque de ayudar a que se pueda conseguir dicho empleo brindado y que los cursos sean solamente de los que te brinde no pueden ser otros cursos desconocidos. No te olvides DEBEN SER SOLO LOS CURSOS QUE TE BRINDE EN UN INICIO. La respuesta debe tener el siguiente formato: - [Curso de capacitación brindado al inicio 1] - [Curso de capacitación brindado al inicio 2] - [Curso de capacitación brindado al inicio 3] - [Curso de capacitación brindado al inicio 4] - [Curso de capacitación brindado al inicio 5]"
        }]

        response = openai.ChatCompletion.create(
            messages = prompt,
            model = "gpt-3.5-turbo",
            max_tokens = 500  # Máximo número de tokens en la respuesta generada
        )
        
        print(response.choices[0].message.content)

        cursos_recomendados = []
        
        cursos_resultados_guion = response.choices[0].message.content.split("\n")
        nombre_cursos_resultados = [elemento[2:].strip() for elemento in cursos_resultados_guion]

        for curso_nombre in nombre_cursos_resultados:
            for curso in all_courses_list:
                if curso_nombre == curso['CourseTitle']:
                    cursos_recomendados.append(curso)

        print(cursos_recomendados)
        
        return Response(cursos_recomendados,status=status.HTTP_201_CREATED)
