from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from authapp.decorators import unauthenticated_user

User = get_user_model()
from authapp.forms import UserRegisterForm, UserLoginForm, ChangePasswordForm
from profilapp.models import Profile
# Create your views here.

@unauthenticated_user
def signup(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data['new_password']
        try:
            user = User.objects.create_user(username,email, password)
            print('work')
            print(user.password)
        except:
            user = None
            print('don\'t work')

        if user != None:
            print('helloooooo')
            login(request, user)
            profile = Profile.objects.create(user = user, email = email, first_name=username)
            messages.success(request, "Account was created for" " "  + username)
            return redirect(reverse('mypost:home'))
        else:
            form = UserRegisterForm()
    
    context = {
        'form':form
    }
    return render(request, 'authapp/signup.html', context)

@unauthenticated_user
def loginUser(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        new_password = form.cleaned_data['new_password']

        user = authenticate(request, username = username, password = new_password)
        print('hello')
        if user != None:
            print('work')
            login(request, user)
            return redirect(reverse('mypost:home'))

        else:
            prin('salut')
            form = UserLoginForm()
            messages.info(request, "Username OR Password is incorrect")

    context = {
    'form':form
    }
    return render(request, 'authapp/login.html', context)


@login_required
def logoutUser(request):
    username = request.user.username
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You're login out", username)
        return redirect(reverse('authapp:account_login'))
    
    return render(request, 'authapp/snippet.html')


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'authapp/change_password.html', context)



def PasswordChangeDone(request):
    messages.info('request', 'Your password has been succesfully changed')
    return HttpResponseRedirect(reverse('authapp:account_login'))
	# return render(request, 'authapp/change_password_done.html')
