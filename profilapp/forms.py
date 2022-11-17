from django import forms
from .models import Profile


class EditProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
    
	first_name = forms.CharField(widget=forms.TextInput(
        attrs={
                 'class': 'form-control'}
                 )
            , max_length=50, required=False)

	last_name = forms.CharField(widget=forms.TextInput(
        attrs={
                 'class': 'form-control'
            })
            , max_length=50, required=False)

	location = forms.CharField(widget=forms.TextInput(
        attrs={
                 'class': 'form-control'
            })
            , max_length=25, required=False)

	url = forms.URLField(widget=forms.TextInput(
        attrs={
                 'class': 'form-control'
            })
            , max_length=60, required=False)

	profile_info = forms.CharField(widget=forms.Textarea(
        attrs={
                 'class': 'form-control'
            })
    , max_length=260, required=False)

	class Meta:
		model = Profile
		fields = ('picture', 'first_name', 'last_name', 'location', 'url', 'profile_info')