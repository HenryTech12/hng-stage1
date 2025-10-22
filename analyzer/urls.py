from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('',SaveAnalyzerView.as_view(), name='save_data'),
    path('<str:id>',FetchAnalyzerView.as_view(), name="fetch_specific_data"),
    path('',SaveAnalyzerView.as_view(), name='fetch_all'),
    path('<str:id>',FetchAnalyzerView.as_view(),name="delete_data"),
    path('filter-by-natural-language',NaturalLanguageFilterAPIView.as_view(),name="natural_filtering")
]
