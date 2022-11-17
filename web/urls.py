from django.urls import path

from . import views

urlpatterns = [
    path('', views.ConnectionPage.as_view(), name='index'),
    path('tables/<str:conn_id>/', views.Tables.as_view(), name='tables'),
    # path('tables/', views.Tables.as_view(), name='tables'),
    # path('job-history/', views.JobHistory.as_view(), name='job-history'),
]