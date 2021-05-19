from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from .models import Lead,Agent
from .forms import LeadForm , LeadModelForm

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

def landingpage(request):
    return render(request,'landingpage.html')


def leadcreate(request):
    form = LeadModelForm()
    if request.method == "POST":
        print('Recieveing a post req')
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form':form #Passing form as a context
    }
    return render(request,'leadcreate.html',context)

def leadupdate(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context={
        'form':form,
        'lead':lead
    }
    return render(request,'leadupdate.html',context)

def leaddelete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')
