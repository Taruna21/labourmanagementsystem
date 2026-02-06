from django import forms
from django.contrib.auth.models import User
from . models import Profile



class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    city = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.RadioSelect)
    area = forms.CharField(max_length=100)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.city = self.cleaned_data['city']
            profile.area = self.cleaned_data['area']
            profile.save()
        return user
        
        
