from django.urls import path
from . import views

urlpatterns = [
    path('', views.Crawl.as_view()),
    path('lam', views.Lam.as_view()),
    path('trieu', views.Trieu.as_view()),
]