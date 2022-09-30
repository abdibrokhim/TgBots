from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('clients/', views.TGClientList.as_view()),
    path('clients/<int:pk>/', views.TGClientDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
