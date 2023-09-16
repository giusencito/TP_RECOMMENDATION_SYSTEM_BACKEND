"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from  django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import re_path,path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.user.views import (Login)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
schema_view = get_schema_view(
   openapi.Info(
      title="Documentación de API",
      default_version='v0.1',
      description="Documentación de API ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="developerpeperu@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('user/',include('apps.user.api.router')),
    path('adminsite/',include('apps.admins.api.router')),
    path('typetest/',include('apps.typetest.api.router')),
    path('tests/',include('apps.tests.api.router')),
    path('section/',include('apps.section.api.router')),
    path('question/',include('apps.question.api.router')),
    path('option/',include('apps.option.api.router')),
    path('postulant/',include('apps.postulants.api.router')),
    path('resultTest/',include('apps.resultTest.api.router')),
    path('resultSection/',include('apps.resultSection.api.router')),
    path('linkedinJob/',include('apps.linkedinJobs.api.router')),
    path('selectedJob/',include('apps.selectedjob.api.router')),
    path('feedback/',include('apps.feedback.api.router')),
    path('course/',include('apps.course.api.router')),
    path('interviewquestions/',include('apps.InterviewQuestions.api.router')),
    path('recomendation/',include('apps.recomendation.api.router')),
    path('courserecomendation/',include('apps.courserecomendation.api.router')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',Login.as_view(), name = 'login'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
