from django.shortcuts import render
from django.http import request,HttpResponse
from .models import Lead

# Create your views here.
def homepage(request):
    # return HttpResponse('Test')
    leads = Lead.objects.all()
    context = {
        'leads':leads
    }
    return render(request,'homepage.html',context)
