from django.urls import path
from .views import leadlist,leaddetail,leadcreate,leadupdate,leaddelete

app_name = "leads"

urlpatterns = [
    path('',leadlist),
    path('<int:pk>/',leaddetail),
    path('<int:pk>/update/',leadupdate),
    path('<int:pk>/delete/',leaddelete),
    path('create/',leadcreate),
]
