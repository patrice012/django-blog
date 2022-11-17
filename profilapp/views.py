from django.shortcuts import render, redirect, reverse
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.views.generic.base import TemplateView

from mypost.models import Post

from profilapp.models import Profile
from profilapp.forms import EditProfileForm

# Create your views here.

# @login_required
def profil(request, uuid):
    ReaderProfil = Profile.objects.get(id = uuid)
    return render(request, 'profilapp/profil.html', {'ReaderProfil': ReaderProfil})


def profilpage(request):
    return render(request, 'profilapp/profile.html',)


# class ProfileCreateView(CreateView):
#     model = Profile
#     template_name = "profilapp/edit_profile.html"
#     form_class = EditProfileForm
#     # fields = ['first_name', 'last_name', 'location', 'url','profile_info','picture']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Create Profile'
#         return context

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.save()
#         return redirect(reverse('mypost:home'))


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profilapp/edit_profile.html"
    form_class = EditProfileForm
    # fields = ['first_name', 'last_name', 'location', 'url','profile_info','picture']

    def get_context_data(self, **kwargs):
        user = self.request.user.id
        profile = Profile.objects.get(user__id=user)
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Profile'
        context['user'] = user
        context['profile'] = profile
        return context

    def form_valid(self, form):
        user_id = self.request.user.id
        profile = Profile.objects.get(user__id=user_id)
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('profilapp:profile', kwargs = {'pk': profile.id}))


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profilapp/profil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_view' in self.request.session:
            last_post_view = Post.objects.all().\
                filter(id = self.request.session["last_view"])
            context['last_post_view'] = last_post_view
        return context
    

    

