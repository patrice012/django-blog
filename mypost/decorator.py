import os
from django.conf import settings
from django.shortcuts import render, redirect, reverse


def un_authenticated_user(class_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return class_func(request, *args, **kwargs)
    return wrapper_func