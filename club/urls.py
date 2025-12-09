# club/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

   # Admin dashboard & CRUD
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('resource/add/', views.resource_create, name='resource_create'),
    path('resource/<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('resource/<int:pk>/delete/', views.resource_delete, name='resource_delete'),

    # Resource CRUD
    path('resources/create/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),

    # Unit CRUD
    path('unit/add/', views.unit_create, name='unit_create'),
    path('unit/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
    path('unit/<int:pk>/delete/', views.unit_delete, name='unit_delete'),
    path('years/<int:year_id>/units/', views.units_by_year, name='units_by_year'),

    # Event CRUD
    path('event/add/', views.event_create, name='event_create'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Academic years
    path('academic-years/', views.academic_years_view, name='academic_years'),
    path('academic-years/', views.academic_year_list, name='academic_year_list'),
    path('academic-years/<int:year_id>/', views.units_by_year, name='units_by_year'),

    # Study resources
    path('resources/', views.study_resources, name='study_resources'),
    path('resources/<str:category>/', views.resources_by_category, name='resources_by_category'),

    path('study-resources/', views.study_resources, name='study_resources'),
    path('past-papers/', views.past_papers, name='past_papers'),
]