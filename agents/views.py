from django.shortcuts import render,reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
# Create your views here.

class AgentListView(LoginRequiredMixin,generic.ListView):
    template_name = "agentlist.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = 'agentcreate.html'
    form_class = AgentModelForm
    def get_success_url(self):
        return '/agents'

    def form_valid(self,form):
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = 'agentdetail.html'
    context_object_name = 'agent'
    def get_queryset(self):
        # return Agent.objects.all()
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'agentupdate.html'
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return '/agents'

class AgentDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'agentdelete.html'
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return '/agents'

    