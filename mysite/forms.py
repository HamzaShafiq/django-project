from django.forms import ModelForm
from django import forms

from django.contrib.auth import get_user_model

from mysite.models import Project, ProjectBid

User = get_user_model()


class UserRegistrationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_role']


class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'user_role']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

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


class ProjectBidForm(ModelForm):
    class Meta:
        model = ProjectBid
        fields = ['amount']


class AssignProjectForm(forms.Form):
    selected_user = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        users_list = initial_arguments.get('users_list', None)
        super(AssignProjectForm, self).__init__(*args, **kwargs)
        self.fields['selected_user'] = forms.ChoiceField(choices=users_list)