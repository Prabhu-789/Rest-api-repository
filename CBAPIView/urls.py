from django.contrib import admin
from django.urls import path
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Gayatri College Students Data",
      default_version='v1',
      description="Student name register",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studentapi/', views.StudentList.as_view()),
    path('students_create/', views.StudentCreate.as_view()),
    path('students_retrieve/<int:pk>/', views.StudentRetrieve.as_view()),
   #  path('students_update/<int:pk>/', views.StudentUpdate.as_view()),
    path('students_update/<int:pk>/', views.StudentUpdate.as_view(), name='student-update'),
    path('students_destroy/<int:pk>/', views.StudentDestroy.as_view()),
   #  path('students_list_create/', views.StudentListCreate.as_view()),
    #path('students_search/', views.StudentSearch.as_view()),
    path('students/search/', views.StudentSearchView.as_view(), name='student-search'),
   #  path('student_retrieve_update/<int:pk>/', views.StudentRetrieveUpdate.as_view()),
   #  path('student_retrieve_destroy/<int:pk>/', views.StudentRetrieveDestroy.as_view()),
   #  path('student_retrieve_update_destroy/<int:pk>/', views.StudentRetrieveUpdateDestroy.as_view()),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
