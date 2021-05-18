from django.urls import path
from .views import leadlist,leaddetail,leadcreate

app_name = "leads"

urlpatterns = [
    path('',leadlist),
    path('<int:pk>/',leaddetail),
    path('create/',leadcreate),
]
