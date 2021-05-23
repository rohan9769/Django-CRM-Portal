from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from .models import Lead,Agent,Category
from .forms import LeadForm , LeadModelForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm
from django.core.mail import send_mail

from django.views import generic

from django.contrib.auth import mixins
from agents.mixins import OrganiserAndLoginRequiredMixin

 

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
    # queryset = Lead.objects.all()
    context_object_name = 'leads'
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile,agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile,agent__isnull=True)
            context.update({
                "unassigned_leads":queryset
            })
        return context
            

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
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset








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

class LeadCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
    template_name = "leadcreate.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return '/leads'
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
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

class LeadUpdateView(OrganiserAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'leadupdate.html'
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return '/leads'



def leaddelete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

class LeadDeleteView(OrganiserAndLoginRequiredMixin,generic.DeleteView):
    template_name = 'leaddelete.html'
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    

    def get_success_url(self):
        return '/leads'


class AssignAgentView(OrganiserAndLoginRequiredMixin,generic.FormView):
    template_name = "assignagent.html"
    form_class = AssignAgentForm
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return '/leads'
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(mixins.LoginRequiredMixin,generic.ListView):

    template_name = 'categorylist.html'
    context_object_name = "categorylist"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDetailView(mixins.LoginRequiredMixin,generic.DetailView):
    template_name = 'categorydetail.html'
    context_object_name = 'category'

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #     context.update({
    #         "leads": leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class LeadCategoryUpdateView(mixins.LoginRequiredMixin,generic.UpdateView):
    template_name = 'leadcategoryupdate.html'
    form_class = LeadCategoryUpdateForm


    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        return '/leads'

