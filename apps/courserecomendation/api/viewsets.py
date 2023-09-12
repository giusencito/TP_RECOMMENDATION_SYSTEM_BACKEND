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

    openai.api_key = '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' #verificar


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

        expert_tips = ['Prepararse para una buena entrevista laboral', 'Tener Experiencia','Desarrollar un buen CV', 'Tener competencias blandas', 'Tener competencias tecnicas', 'Tener valores y principios']
        prompt = [{ "role": "user",
           "content": f"Se tienen los siguientes cursos de capacitación: {cursos_solo_titulos}  Ahora te voy a pasar unos tips o consejos para conseguir un empleo de ingeniero de Software dados por un experto: {expert_tips}  Finalmente, te voy a pasar el nombre de un empleo: {job.jobName}  y su respectiva descripción: {job.jobDescription} Ahora con toda la información obtenida necesito que me recomiendes los mejores 5 cursos NO TECNICOS de capacitación para este empleo basándote en los nombres de los cursos que te brinde en un inicio, los tips o consejos para conseguir un empleo de ingeniero de Software dados por el experto y la descripcion del empleo. Recuerda que los cursos que me recomiendes deben tener el objetivo de ayudar a que se pueda conseguir dicho empleo brindado y que los cursos sean solamente de los que te brinde no pueden ser otros cursos desconocidos. No te olvides DEBEN SER SOLO LOS CURSOS QUE TE BRINDE EN UN INICIO. La respuesta debe tener el siguiente formato: - [Curso de capacitación brindado al inicio 1] - [Curso de capacitación brindado al inicio 2] - [Curso de capacitación brindado al inicio 3] - [Curso de capacitación brindado al inicio 4] - [Curso de capacitación brindado al inicio 5]. RECUERDA GPT SIGUE EL FORMATO TIENE QUE TENER SI O SI ESE FORMATO"
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

    @action(detail=True, methods=['post'])
    def QuestionRecomendation(self, request,pk=None):
        job_id = pk
        print(job_id)
        
        job = get_object_or_404(LinkedinJobs, pk=job_id)
        print(type(job))
        print(job.jobName)
        print(job.jobDescription)

        prompt = [{ "role": "user",
           "content": f"Soy ingeniero de software en {job.jobLocation} y estoy postulando a {job.jobName} que tiene la siguiente descripción: {job.jobDescription} me puedes indicar 5 preguntas claves con sus respectivas respuestas para una entrevista laboral en esta especialidad Necesito que me des la respuesta con el siguiente formato: Preguntas [Aqui va la pregunta 1] [Aqui va la pregunta 2] [Aqui va la pregunta 3] [Aqui va la pregunta 4] [Aqui va la pregunta 5] Respuestas: [Aqui va la respuesta de la pregunta 1] [Aqui va la respuesta de la pregunta 2] [Aqui va la respuesta de la pregunta 3] [Aqui va la respuesta de la pregunta 4] [Aqui va la respuesta de la pregunta 5] NO TE OLVIDES QUE TIENES QUE RESPETAR EL FORMATO. Tambien recuerda que la respuesta de cada pregunta debe ser la mas corta, concreta y directa para poder responder la pregunta"
        }]

        response = openai.ChatCompletion.create(
            messages = prompt,
            model = "gpt-3.5-turbo",
            max_tokens = 500  # Máximo número de tokens en la respuesta generada
        )

        print(response.choices[0].message.content)
        print(type(response.choices[0].message.content))

        lines = response.choices[0].message.content.strip().split("\n")
        lines = [line for line in lines if line.strip() != ""]

        preguntasrespuestas = lines 

        print("Estas son las preguntas y respuestas")
        print(preguntasrespuestas)

        return Response(preguntasrespuestas,status=status.HTTP_201_CREATED)