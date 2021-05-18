from django.urls import path
from .views import leadlist,leaddetail

app_name = "leads"

urlpatterns = [
    path('',leadlist),
    path('<pk>/',leaddetail)
]
