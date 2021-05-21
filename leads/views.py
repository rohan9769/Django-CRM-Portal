from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from .models import Lead,Agent
from .forms import LeadForm , LeadModelForm,CustomUserCreationForm
from django.core.mail import send_mail

from django.views import generic

from django.contrib.auth import mixins

 

# Create your views here.

class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return '/login'


def landingpage(request):
    return render(request,'landingpage.html')


class LandingPageView(generic.TemplateView):
    template_name = "landingpage.html"



class LeadListView(mixins.LoginRequiredMixin,generic.ListView):
    template_name = "leadlist.html"
    queryset = Lead.objects.all()
    context_object_name = 'leads'


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

class LeadDetailView(mixins.LoginRequiredMixin,generic.DetailView):
    template_name = "leaddetail.html"
    queryset = Lead.objects.all()
    context_object_name = 'lead'







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

class LeadCreateView(mixins.LoginRequiredMixin,generic.CreateView):
    template_name = "leadcreate.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return '/leads'
    
    def form_valid(self, form):
        send_mail(
            subject="Lead has been created" , 
            message="Go to the leads list page to see the new lead",
            from_email="abc@xyz.com",
            recipient_list=["abc@xyz.com"]
        )
        return super(LeadCreateView,self).form_valid(form)




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

class LeadUpdateView(mixins.LoginRequiredMixin,generic.UpdateView):
    template_name = 'leadupdate.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return '/leads'



def leaddelete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

class LeadDeleteView(mixins.LoginRequiredMixin,generic.DeleteView):
    template_name = 'leaddelete.html'
    queryset = Lead.objects.all()
    

    def get_success_url(self):
        return '/leads'
