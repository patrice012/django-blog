from django.shortcuts import render, redirect, reverse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('mypost:home'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func