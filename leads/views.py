from django.shortcuts import render
from django.http import request,HttpResponse
from .models import Lead

# Create your views here.
def leadlist(request):
    # return HttpResponse('Test')
    leads = Lead.objects.all()
    context = {
        'leads':leads
    }
    return render(request,'leadlist.html',context)

def leaddetail(request,pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead':lead
    }
    return render(request,'leaddetail.html',context)
