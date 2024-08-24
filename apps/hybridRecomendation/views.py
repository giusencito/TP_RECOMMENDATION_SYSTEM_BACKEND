from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from rest_framework.decorators import action
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import Dataset, Reader, SVD
from surprise.prediction_algorithms import KNNBasic
from surprise.model_selection import train_test_split
import json
from apps.linkedinJobs.models import LinkedinJobs
from apps.linkedinJobs.api.serializer import LinkedinJobsSerializer
from apps.resultTest.api.serializer import ResultTestSerializer
from django.shortcuts import get_object_or_404
from apps.resultTest.models import ResultTest
import time
# Create your views here.
class HybridRecomendationViewset(viewsets.ModelViewSet):
      start = 0
      jobs_per_page = 25
      total_jobs = 25
      data = []
      model = LinkedinJobs
      serializer_class = LinkedinJobsSerializer
      BackendUrl=   f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20Backend&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start=0"
      FrontendUrl=  f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20Frontend&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start=0"
      FullStackUrl =f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20Fullstack&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start=0"
      MobileUrl =   f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20M%C3%B3vil&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start=0"
      DataUrl =     f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Ingenier%C3%ADa%20de%20datos&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start=0"
      def GetText(self,job,tag,class_name):
          element = job.find(tag, class_=class_name)
          return element.text.strip() if element else "Text not found"
      def GetURL(self,job):
          url_element = job.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
          if url_element is None:
             url_element = job.find('a', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
          return url_element['href'] if url_element else "URL not found"
      def GetPublishDate(self,job):
          publish_date_element = job.find('time',class_='job-search-card__listdate')
          if not publish_date_element:
             publish_date_element = job.find('time',class_='job-search-card__listdate--new')
          return publish_date_element.text.strip() if publish_date_element else "Publication date not found"
      def GetDescription(self,url):
          job_response = requests.get(url)
          job_soup = BeautifulSoup(job_response.text, 'html.parser')
          description_boxes = job_soup.find_all('div',class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden')
          if not description_boxes:
                return "Description not found"
          return "\n".join(
                [p.strip() for box in description_boxes for p in box.strings if p.strip()]
          )
      def GetJobv2(self,url,file):
          dataJob=[]
          max_retries = 5
          while self.start < self.total_jobs:
                for attempt in range(max_retries):
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    jobs = soup.find_all('li')
                    if jobs:
                        break
                    else:
                        print(f"No jobs found on attempt {attempt + 1}. Retrying...")
                        time.sleep(1)
                if not jobs:
                   print(f"No jobs found on page")
                   continue
                for job in jobs:
                    title = self.GetText(job, 'h3', 'base-search-card__title')
                    location = self.GetText(job, 'span', 'job-search-card__location')
                    job_url = self.GetURL(job)
                    job_company = self.GetText(job, 'h4', 'base-search-card__subtitle')
                    publish_date = self.GetPublishDate(job)
                    description = self.GetDescription(job_url)
                    dataJob.append([title, job_url, location, publish_date, job_company, description])
                self.start += self.jobs_per_page
          self.start=0
          df = pd.DataFrame(dataJob, columns=['JobName', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv(file ,sep='\t',index=False)


    
      def GetJob(self,url,file):
          dataJob=[]
          while self.start < self.total_jobs:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = soup.find_all('li')
                while len(jobs) ==0:
                      response = requests.get(url)
                      soup = BeautifulSoup(response.text, 'html.parser')
                      jobs = soup.find_all('li')
                for job in jobs:
                    title = self.GetText(job, 'h3', 'base-search-card__title')
                    location = self.GetText(job, 'span', 'job-search-card__location')
                    job_url = self.GetURL(job)
                    job_company = self.GetText(job, 'h4', 'base-search-card__subtitle')
                    publish_date = self.GetPublishDate(job)
                    description = self.GetDescription(job_url)
                    dataJob.append([title, job_url, location, publish_date, job_company, description])
                self.start += self.jobs_per_page
          self.start=0
          df = pd.DataFrame(dataJob, columns=['JobName', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv(file ,sep='\t',index=False)
      
      
      def DefineJob(self,job):
           url = self.GetURL(job)
           return {
            'JobName': self.GetText(job, 'h3', 'base-search-card__title'),
            'URL': url,
            'Location': self.GetText(job, 'span', 'job-search-card__location'),
            'Date': self.GetPublishDate(job),
            'Company': self.GetText(job, 'h4', 'base-search-card__subtitle'),
            'Description': self.GetDescription(url)
        }

      @action(detail=False, methods=['get'])
      def getAllJobs(self,request):
          self.GetJobv2(self.BackendUrl,'csv/Backendjobs.csv')
          self.GetJobv2(self.FrontendUrl,'csv/Frontendjobs.csv')
          self.GetJobv2(self.FullStackUrl,'csv/Fullstackjobs.csv')
          self.GetJobv2(self.MobileUrl,'csv/Moviljobs.csv')
          self.GetJobv2(self.DataUrl,'csv/Datosjobs.csv')
          archivos_csv = ['csv/Backendjobs.csv', 'csv/Datosjobs.csv', 'csv/Frontendjobs.csv', 'csv/Fullstackjobs.csv', 'csv/Moviljobs.csv']
          dataframes = []
          for archivo in archivos_csv:
              df = pd.read_csv(archivo, sep='\t')
              dataframes.append(df)
          df_unido = pd.concat(dataframes)
          df_unido.insert(0, 'JobId', range(1, len(df_unido) + 1))
          df_unido.to_csv('csv/jobs.csv', sep='\t', index=False, line_terminator='\n')
          df = pd.read_csv('csv/jobs.csv', sep='\t')
          df_head_json =df.head(5).to_json(orient='records')
          return Response(df_head_json)
      def calculate_similarity(self,test_section,test_description,rating):
        if test_section is None or pd.isnull(test_description):
           return 0
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([test_section,test_description])
        similarity = (tfidf_matrix * tfidf_matrix.T).A[0, 1] * rating
        return similarity
      @action(detail=True, methods=['get'])
      def hydridRecommendation(self,request,pk=None):
          jobs_df = pd.read_csv('csv/jobs.csv',sep='\t')
          ratings_df = pd.read_csv('csv/ratings_section.csv')
          sections_df = pd.read_csv('csv/section.csv')
          all_combinations = pd.MultiIndex.from_product([sections_df['SectionId'], jobs_df['JobId']], names=['SectionId', 'JobId'])
          all_combinations_df = pd.DataFrame(index=all_combinations).reset_index()
          merged_df = all_combinations_df.merge(ratings_df, on='SectionId', how='left')
          merged_df = merged_df.merge(sections_df, left_on='SectionId',right_on='SectionId', how='left')
          merged_df = merged_df.merge(jobs_df, left_on='JobId', right_on='JobId', how='left')
          merged_df['DevelopmentPercentage'].fillna(0, inplace=True)
          reader = Reader(rating_scale=(1, 5))
          data = Dataset.load_from_df(merged_df[['SectionName', 'Description', 'DevelopmentPercentage']], reader)
          trainset, testset = train_test_split(data,test_size=0.2, random_state=42)
          knn_model = KNNBasic(sim_options={'name': 'cosine', 'user_based': False})
          knn_model.fit(trainset)
          content_model = SVD()
          content_model.fit(trainset)
          predictions = []
          max_rating = merged_df[ 'DevelopmentPercentage'].max()
          min_rating = merged_df['DevelopmentPercentage'].min()
          for test_section, test_description, test_rating in testset:
              knn_pred = knn_model.predict(test_section,test_description, test_rating).est
              content_pred = content_model.predict(test_section, test_description,test_rating).est
              similarity_pred_content = self.calculate_similarity(test_section,test_description,content_pred)
              similarity_pred_knn =self. calculate_similarity(test_section,test_description,knn_pred)
              similarity_hybrid_pred = min((similarity_pred_content + similarity_pred_knn) / 2, 1.0)
              similarity_hybrid_pred = round(similarity_hybrid_pred, 1)
              section_rating = merged_df.loc[merged_df['SectionName'] == test_section,'DevelopmentPercentage'].iloc[0]
              normalized_rating = (section_rating - min_rating) / (max_rating - min_rating)
              similarity_hybrid_pred *= normalized_rating
              predictions.append((test_section, test_description, test_rating, similarity_hybrid_pred))    
          df_predictions = pd.DataFrame(predictions, columns=['SectionName', 'Description', 'DevelopmentPercentage','Similarity'])
          recommendations = merged_df[['JobId', 'JobName', 'URL', 'Location', 'Date', 'Company','Description']].merge(df_predictions, on='Description')
          recommendations = recommendations.sort_values('Similarity', ascending=False)[['JobName','URL','Location','Date', 'Company', 'Similarity']]
          recommendations = recommendations.drop_duplicates(subset=['JobName'])
          recommendations = recommendations.loc[recommendations['Similarity'] != 0.0]
          top_10_recommendations = recommendations.head(10).copy()
          result_test = get_object_or_404(ResultTest, pk=pk)
          created_jobs = []
          for index, job in top_10_recommendations.iterrows():
              linkedin_job = LinkedinJobs.objects.create(
                    jobName=job["JobName"],
                    jobDescription="",
                    jobUrl=job["URL"],
                    jobLocation=job["Location"],
                    jobCompany=job["Company"],
                    jobDate=job["Date"],
                    posibilityPercentage=job["Similarity"],
                    resultTest=result_test 
              )
              created_jobs.append(LinkedinJobsSerializer(linkedin_job).data)
          recomendations_json= json.dumps(created_jobs)
          recommendations_list = json.loads(recomendations_json)
          return Response(recommendations_list,status=status.HTTP_201_CREATED)