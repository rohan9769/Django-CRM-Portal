from django.urls import path
from .views import leadlist,leaddetail,leadcreate,leadupdate,leaddelete,LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,LeadDeleteView,AssignAgentView,CategoryListView,CategoryDetailView,LeadCategoryUpdateView

app_name = "leads"

urlpatterns = [
    # path('',leadlist),
    path('',LeadListView.as_view()),

    # path('<int:pk>/',leaddetail),
    path('<int:pk>/',LeadDetailView.as_view()),

    # path('<int:pk>/update/',leadupdate),
    path('<int:pk>/update/',LeadUpdateView.as_view()),


    # path('<int:pk>/delete/',leaddelete),
    path('<int:pk>/delete/',LeadDeleteView.as_view()),

    path('<int:pk>/assignagent/',AssignAgentView.as_view(),name='assign-agent'),
    path('<int:pk>/category/',LeadCategoryUpdateView.as_view(),name='lead-category-update'),

    # path('create/',leadcreate),
    path('create/',LeadCreateView.as_view()),
    path('categories/',CategoryListView.as_view()),
    path('categories/<int:pk>/',CategoryDetailView.as_view(),name='category-detail')
]
