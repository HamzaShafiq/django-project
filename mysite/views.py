from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.views.generic import UpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from mysite.forms import UserRegistrationForm, UserProfileForm, ProjectForm, ProjectBidForm, AssignProjectForm
from mysite.models import Project, ProjectBid

User = get_user_model()


def home(request):
    return render(request, 'mysite/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            email = user_obj['email']
            password = user_obj['password']
            user_role = user_obj['user_role']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                # Need recommendation
                user.user_role = user_role
                user.save()
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'mysite/register.html', {'form' : form})


def profile_view(request):
    user = request.user
    return render(request, 'mysite/profile.html', {"user": user})


class EditUserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'mysite/edit_profile.html'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user

    def get_success_url(self, *args, **kwargs):
        return reverse("home")


def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'mysite/change_password.html', {
        'form': form
    })


def project_list(request, template_name='mysite/project_list.html'):
    projects = Project.objects.all()
    data = {'object_list': projects}
    return render(request, template_name, data)


def project_create(request, template_name='mysite/project_form.html'):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.status = 'Unassigned'
        form.save()
        return redirect('project_list')
    return render(request, template_name, {'form': form})


def project_view(request, pk, template_name='mysite/project_view.html'):
    project = get_object_or_404(Project, pk=pk)
    return render(request, template_name, {'project': project})


def project_update(request, pk, template_name='mysite/project_form.html'):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('project_list')
    return render(request, template_name, {'form': form})


def project_delete(request, pk, template_name='mysite/project_confirm_delete.html'):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, template_name, {'object': project})


def project_bid_list(request, template_name='mysite/project_bid_list.html'):
    project_bids = ProjectBid.objects.all()
    data = {'object_list': project_bids}
    return render(request, template_name, data)


def project_bid_create(request, project_id, template_name='mysite/project_bid_form.html'):

    form = ProjectBidForm(request.POST or None)
    projects = Project.objects.all()
    if form.is_valid():
        project_bid = form.save(commit=False)
        project_bid.bid_by = request.user
        project_bid.project = projects.get(pk=project_id)
        form.save()
        return redirect('project_bid_list')
    return render(request, template_name, {'form': form})


def project_bid_update(request, pk, template_name='mysite/project_bid_form.html'):
    project_bid = get_object_or_404(ProjectBid, pk=pk)
    form = ProjectBidForm(request.POST or None, instance=project_bid)
    if form.is_valid():
        form.save()
        return redirect('project_bid_list')
    return render(request, template_name, {'form': form})


def project_bid_delete(request, pk, template_name='mysite/project_bid_confirm_delete.html'):
    project_bid = get_object_or_404(ProjectBid, pk=pk)
    if request.method == 'POST':
        project_bid.delete()
        return redirect('project_bid_list')
    return render(request, template_name, {'object': project_bid})


def project_assign(request, pk, template_name='mysite/project_assign_form.html'):
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