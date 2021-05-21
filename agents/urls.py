from django.urls import path
from .views import AgentListView,AgentCreateView,AgentDetailView,AgentUpdateView,AgentDeleteView
app_name = 'agents'

urlpatterns = [
    path('',AgentListView.as_view(),name='agentlist'),
    path('<int:pk>/',AgentDetailView.as_view(),name='agentdetail'),
    path('<int:pk>/update/',AgentUpdateView.as_view(),name='agentupdate'),
    path('<int:pk>/delete/',AgentDeleteView.as_view()),
    path('create/',AgentCreateView.as_view(),name='agentcreate'),
    
]
