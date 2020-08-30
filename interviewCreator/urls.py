from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.createInterview, name='createInterview'),
    path('interviews', views.viewInterviews, name='interviews'),
    path('participants', views.viewParticipants, name='participants'),
    path('edit/<int:id>', views.editParticipant, name='editParticipant'),
]
