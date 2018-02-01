from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from freelancingsite.forms import UserRegistrationForm, UserProfileForm, ProjectForm, ProjectBidForm, AssignProjectForm
from freelancingsite.models import Project, ProjectBid, USER_ROLES

User = get_user_model()


class Home(TemplateView):
    """ render home page to welcome user """
    template_name = "freelancingsite/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['user_role'] = USER_ROLES
        return context


class Register(View):
    """ render register page to register user """
    form_class = UserRegistrationForm
    template_name = 'freelancingsite/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            authenticate(username=user.username, password=user.password)
            login(self.request, user)
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class ViewProfile(TemplateView):
    """ render profile page to show user profile """
    template_name = 'freelancingsite/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ViewProfile, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class EditUserProfileView(UpdateView):
    """ render edit page to edit user profile """
    model = User
    form_class = UserProfileForm
    template_name = 'freelancingsite/edit_profile.html'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user

    def get_success_url(self, *args, **kwargs):
        return reverse("home")


class ChangePassword(View):
    """ render change password page for changing user password """
    form_class = PasswordChangeForm
    template_name = 'freelancingsite/change_password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')

        return render(request, self.template_name, {'form': form})


class ProjectList(ListView):
    """ render projects page to show all projects """

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = USER_ROLES
        return context


class CreateProject(CreateView):
    """ render form to create project """
    template_name = 'freelancingsite/project_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.save()
        return redirect('project_list')

    def get_form_kwargs(self):
        kwargs = super(CreateProject, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ViewProject(DetailView):
    """ render project page to show a project """
    model = Project
    slug_field = 'pk'
    context_object_name = 'project'
    template_name = "freelancingsite/project_view.html"


class UpdateProject(UpdateView):
    """ render form to update project """
    slug_field = 'pk'
    template_name = 'freelancingsite/project_form.html'
    success_url = '/projects/'
    model = Project
    fields = ['name', 'description']


@csrf_exempt
def project_delete(request):
    """ delete a project via ajax post request """
    if request.method == 'POST':
        if request.is_ajax():
            project_id = request.POST['project_id']
            project = get_object_or_404(Project, pk=project_id)
            project.delete()
            return HttpResponse()
    return render(request)


class ListOfProjectBids(ListView):
    """ render project bid page to show all project and bids on them """
    model = ProjectBid


class CreateBidForProject(CreateView):
    """ render form to create project bid """
    template_name = 'freelancingsite/project_bid_form.html'
    form_class = ProjectBidForm

    def form_valid(self, form):
        form.save()
        return redirect('project_bid_list')

    def get_form_kwargs(self):
        kwargs = super(CreateBidForProject, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['project_id'] = self.kwargs.get('project_id', None)
        return kwargs


class UpdateBidForProject(UpdateView):
    """ render form to update project bid """
    slug_field = 'pk'
    template_name = 'freelancingsite/project_bid_form.html'
    success_url = '/project_bids/'
    model = ProjectBid
    fields = ['amount']


@csrf_exempt
def project_bid_delete(request):
    """ delete a project bid via ajax post request """
    if request.method == 'POST':
        if request.is_ajax():
            bid_id = request.POST['project_bid']
            project_bid = get_object_or_404(ProjectBid, pk=bid_id)
            project_bid.delete()
            return HttpResponse()
    return render(request)


def project_assign(request, pk, template_name='freelancingsite/project_assign_form.html'):
    """ assign a project to a user """
    project = get_object_or_404(Project, pk=pk)
    user_ids = ProjectBid.objects.all().filter(project=project).values_list('bid_by', flat=True)
    users = User.objects.filter(pk__in=list(user_ids))

    form = AssignProjectForm(request.POST or None, initial={'users_list': list(users.values_list('id', 'username'))
})
    if form.is_valid():
        form_data = form.cleaned_data
        user_id = form_data['selected_user']
        user = get_object_or_404(User, pk=user_id)
        project.assigned_to = user.username
        project.status = 'Assigned'
        project.save()
        return redirect('project_list')
    return render(request, template_name, {'form': form})

