from django.urls import path

from . import views


urlpatterns = [
    path('reports/', views.all_reports, name='reports'),
    path('reports/<uuid:uuid>/', views.report, name='retrieve-report'),
    path('transactions/', views.transactions, name='transactions')
]
