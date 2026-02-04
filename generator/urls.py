from django.urls import path
from . import views  # <--- THIS IS THE MISSING LINE

urlpatterns = [
    path('', views.search_view, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<int:emp_id>/', views.delete_employee, name='delete_employee'), # New line
    path('resume/', views.generate_resume, name='generate_resume'), # Updated line
]