import random
from django.shortcuts import render,reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin
from django.core.mail import send_mail
# Create your views here.

class AgentListView(OrganiserAndLoginRequiredMixin,generic.ListView):
    template_name = "agentlist.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganiserAndLoginRequiredMixin,generic.CreateView):
    template_name = 'agentcreate.html'
    form_class = AgentModelForm
    def get_success_url(self):
        return '/agents'

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f'{random.randint(0,100000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
            
        )
        send_mail(
            subject = "You have been invited for being an agent",
            message = "You were added as an agent on the CRM Portal.Please Login to start working",
            from_email = "admin@test.com",
            recipient_list = [user.email]
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganiserAndLoginRequiredMixin,generic.DetailView):
    template_name = 'agentdetail.html'
    context_object_name = 'agent'
    def get_queryset(self):
        # return Agent.objects.all()
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganiserAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'agentupdate.html'
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return '/agents'

class AgentDeleteView(OrganiserAndLoginRequiredMixin,generic.DeleteView):
    template_name = 'agentdelete.html'
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return '/agents'


