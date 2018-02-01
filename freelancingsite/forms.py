from django.db.models import Q
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponseRedirect

from freelancingsite.models import Project, ProjectBid

User = get_user_model()


class UserRegistrationForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_role']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        if not (User.objects.filter(Q(username=user.username), Q(email=user.email)).exists()):
            if commit:
                user.save()
            return user
        else:
            raise forms.ValidationError('Looks like a user with that email or username already exists')


class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'user_role']

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProjectForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        project.created_by = self.request.user
        project.status = 'Unassigned'
        if commit:
            project.save()
        return project


class ProjectBidForm(ModelForm):
    class Meta:
        model = ProjectBid
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.project_id = kwargs.pop('project_id')
        super(ProjectBidForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        project_bid = super(ProjectBidForm, self).save(commit=False)
        projects = Project.objects.all()
        project_bid.bid_by = self.request.user
        project_bid.project = projects.get(pk=self.project_id)
        if commit:
            project_bid.save()
        return project_bid


class AssignProjectForm(forms.Form):
    selected_user = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        users_list = initial_arguments.get('users_list', None)
        super(AssignProjectForm, self).__init__(*args, **kwargs)
        self.fields['selected_user'] = forms.ChoiceField(choices=users_list)

