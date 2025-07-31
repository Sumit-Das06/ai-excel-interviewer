# excel_interviewer_project/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure to import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('interviewer.urls')), # Add this line
]
