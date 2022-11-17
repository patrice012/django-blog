from  django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.Form):
    username = forms.CharField(
        label = "Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={'required': True,
                 'class': 'form-control'}
        )
    )

    email = forms.EmailField(
        label = "E-mail",
        widget=forms.EmailInput(
            attrs={'required': True,
                 'class': 'form-control'}
        )
    )

    new_password= forms.CharField(
        label = "Mots de passe",
        widget=forms.PasswordInput(
            attrs={'required': True,
                 'class': 'form-control'}
        )
    )


    confirm_password= forms.CharField(
        label = "confirmer le mot depasse",
        widget=forms.PasswordInput(
            attrs={'required': True,
                 'class': 'form-control'}
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact = username)
        if qs.exists():
            raise forms.ValidationError('This is an invalid username, please pick another!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact = email)
        if qs.exists():
            raise forms.ValidationError('This email is already in use! Please pick another')
        return email

    # def clean_password(self):
    #     new_password = self.cleaned_data.get('new_password')
    #     print(new_password)
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #     print(confirm_password)

    #     if new_password != confirm_password:
    #         raise forms.ValidationError('Password don\'t match')

    #     return new_password

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label = "Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={'required': True,
                 'class': 'form-control'}
        )
    )

    new_password = forms.CharField(
        label = "Mots de passe",
        widget=forms.PasswordInput(
            attrs={'required': True,
                 'class': 'form-control'}
        )
    )

    remember = forms.BooleanField(
        required=False,
        label = "Se souvenir de moi"
        )


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('new_password')
        print(password)
        qs = User.objects.filter(username__iexact = username)
        if not qs.exists():
            print('exist')
            raise forms.ValidationError('User does not exist!')

        if username and password:
            user = authenticate( username = username, password = password)

            if not user:
                print('does not exist')
                raise forms.ValidationError('This user does not exist!')

            if not user.check_password(password):
                print('incorrect password')
                raise forms.ValidationError('Incorrect password')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    

class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'input is-medium'}), 
                                    label="Old password", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'input is-medium'}), 
                                    label="New password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'input is-medium'}), 
                                    label="Confirm new password", required=True)

    class Meta:
            model = User
            fields = ('id', 'old_password', 'new_password', 'confirm_password')


    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['Passwords do not match.'])
        return self.cleaned_data




