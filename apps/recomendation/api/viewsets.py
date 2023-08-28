from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from rest_framework.decorators import action
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise.prediction_algorithms import KNNBasic
from surprise import accuracy
class RecomendationViewset(viewsets.ModelViewSet):
      start = 0
      jobs_per_page = 25
      total_jobs = 25
      data = []
      
      def GetJob(self,url):
          while self.start < self.total_jobs:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = soup.find_all('li')
                for job in jobs:
                    title = job.find('h3', class_='base-search-card__title').text.strip()
                    url_element = job.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
                    if url_element is not None:
                       job_url = url_element['href']
                    else:
                       url_element = job.find('a', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
                       if url_element is not None:
                          job_url = url_element['href']
                       else:
                          job_url = "URL not found"
                    location = job.find('span', class_='job-search-card__location').text.strip()
                    publishdate_element = job.find('time',class_='job-search-card__listdate')
                    if publishdate_element is not None:
                       publishdate = publishdate_element.text.strip()
                    else:
                       publishdate_element = job.find('time',class_='job-search-card__listdate--new')
                    if publishdate_element is not None:
                       publishdate = publishdate_element.text.strip()
                    else:
                       publishdate = "Publication date not found"
                    jobcompany = job.find('h4',class_='base-search-card__subtitle').text.strip()
                    job_response = requests.get(job_url)
                    job_soup = BeautifulSoup(job_response.text, 'html.parser')
                    description_boxes = job_soup.find_all('div',class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden')
                    if len(description_boxes) == 0:
                      continue
                    ul_texts = []
                    for box in description_boxes:
                        string_texts = [p.strip() for p in box.strings if p.strip() != '']
                        ul_texts.extend(string_texts)
                    self.data.append([title, job_url,location,publishdate,jobcompany, "\n".join(ul_texts)])
                self.start += self.jobs_per_page
      def getBackendJobs(self):
          url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20Backend&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start={self.start}"
          self.GetJob(url)
          self.start=0
          df = pd.DataFrame(self.data, columns=['Jobname', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv('csv/Backendjobs.csv', sep='\t',index=False)
      def getFrontendJobs(self):
          url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20Frontend&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start={self.start}"
          self.GetJob(url)
          self.start=0
          df = pd.DataFrame(self.data, columns=['Jobname', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv('csv/Frontendjobs.csv', sep='\t',index=False)
      def getFullSatckJobs(self):
          url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20Fullstack&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start={self.start}"
          self.GetJob(url)
          self.start=0
          df = pd.DataFrame(self.data, columns=['Jobname', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv('csv/Fullstackjobs.csv', sep='\t',index=False)
      def getMobileJobs(self):
          url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Desarrollador%20M%C3%B3vil&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start={self.start}"
          self.GetJob(url)
          self.start=0
          df = pd.DataFrame(self.data, columns=['Jobname', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv('csv/Moviljobs.csv', sep='\t',index=False)
      def getDataJobs(self):
          url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Ingenier%C3%ADa%20de%20datos&location=Lima%2C%20Per%C3%BA&f_TPR=r2592000&geoId=100829422&trk=public_jobs_jobs-search-bar_search-submit&refresh=true&start={self.start}"
          self.GetJob(url)
          self.start=0
          df = pd.DataFrame(self.data, columns=['Jobname', 'URL', 'Location', 'Date', 'Company', 'Description'])
          df.to_csv('csv/Datosjobs.csv', sep='\t',index=False)
      
      
      
      @action(detail=False, methods=['get'])
      def getAllJobs(self,request):
          self.getBackendJobs()
          self.getFrontendJobs()
          self.getFullSatckJobs()
          self.getMobileJobs()
          self.getDataJobs()
          archivos_csv = ['csv/Backendjobs.csv', 'csv/Datosjobs.csv', 'csv/Frontendjobs.csv', 'csv/Fullstackjobs.csv', 'csv/Moviljobs.csv']
          dataframes = []
          for archivo in archivos_csv:
              df = pd.read_csv(archivo, sep='\t')
              dataframes.append(df)
          df_unido = pd.concat(dataframes)
          df_unido.insert(0, 'Jobid', range(1, len(df_unido) + 1))
          df_unido.to_csv('csv/jobs.csv', sep='\t', index=False, line_terminator='\n')
          df = pd.read_csv('csv/jobs.csv', sep='\t')
          df_head_json =df.head(5).to_json(orient='records')
          print(df.head(5))
          return Response(df_head_json)
      @action(detail=False, methods=['post'])
      def hydridRecommendation(self,request):
          jobs_df = pd.read_csv('csv/jobs.csv',sep='\t')
          ratings_df = pd.read_csv('csv/ratings_section.csv')
          sections_df = pd.read_csv('csv/section.csv')
          all_combinations = pd.MultiIndex.from_product([sections_df['id'], jobs_df['Jobid']], names=['sectionId', 'Jobid'])
          all_combinations_df = pd.DataFrame(index=all_combinations).reset_index() 
          merged_df = all_combinations_df.merge(ratings_df, on='sectionId', how='left')
          merged_df = merged_df.merge(sections_df, left_on='sectionId', right_on='id', how='left')
          merged_df = merged_df.merge(jobs_df, left_on='Jobid', right_on='Jobid', how='left')
          merged_df.dropna(subset=['rating'], inplace=True)
          reader = Reader(rating_scale=(1, 5))
          data = Dataset.load_from_df(merged_df[['sectionname', 'Description', 'rating']], reader)
          trainset, testset = train_test_split(data,test_size=0.2)
          knn_model = KNNBasic()
          knn_model.fit(trainset)
          content_model = SVD()
          content_model.fit(trainset)
          predictions = []
          max_rating = merged_df['rating'].max()
          min_rating = merged_df['rating'].min()
          for test_section, test_description, test_rating in testset:
              knn_pred = knn_model.predict(test_section, test_description, test_rating).est
              content_pred = content_model.predict(test_section, test_description, test_rating).est
              similarity_pred_content = self.calculate_similarity({'sectionname': test_section, 'Description': test_description, 'rating': content_pred})
              similarity_pred_knn = self.calculate_similarity({'sectionname': test_section, 'Description': test_description, 'rating': knn_pred})
              similarity_hybrid_pred = min((similarity_pred_content + similarity_pred_knn) / 2, 1.0)
              similarity_hybrid_pred = round(similarity_hybrid_pred, 1)
              section_rating = merged_df.loc[merged_df['sectionname'] == test_section, 'rating'].iloc[0]
              normalized_rating = (section_rating - min_rating) / (max_rating - min_rating)
              similarity_hybrid_pred *= normalized_rating
              predictions.append((test_section, test_description, test_rating, similarity_hybrid_pred))
          df_predictions = pd.DataFrame(predictions, columns=['sectionname', 'Description', 'rating','similarity_pred'])
          recommendations = merged_df[['Jobid', 'Jobname', 'URL', 'Location', 'Date', 'Company','Description']].merge(df_predictions, on='Description')
          recommendations = recommendations.sort_values('similarity_pred', ascending=False)[['Jobname','Description','URL', 'Location','Date', 'Company', 'similarity_pred']]
          recommendations = recommendations.drop_duplicates(subset=['Jobname'])
          recommendations = recommendations.loc[recommendations['similarity_pred'] != 0.0]
          recomendations_json= recommendations.to_json(orient='records')
          recommendations_list = json.loads(recomendations_json)
          return Response(recommendations_list,status=status.HTTP_201_CREATED)
              

      def calculate_similarity(self,row):
        sectionname = row['sectionname']
        description = row['Description']
        if sectionname is None or pd.isnull(description):
           return 0
        else:
           rating = row['rating']
           similarity = description.lower().count(sectionname.lower()) * rating
           return similarity

        

          
          
          



          
    