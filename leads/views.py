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

# def leadcreate(request):
#     form = LeadForm()
#     if request.method == "POST":
#         print('Recieveing a post req')
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name = first_name,
#                 last_name = last_name,
#                 age = age,
#                 agent = agent,
#             )
#             return redirect('/leads')
#     context = {
#         'form':form #Passing form as a context
#     }
#     return render(request,'leadcreate.html',context)

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
