from django.db.models import Count, Q
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

from profilapp.models import Profile

from mypost.models import Post, PostView, Comment
from mypost.forms import PostForm, CommentForm
from mypost.decorator import un_authenticated_user

# from profilapp.models import ReaderProfil, AuthorProfil

from django.conf import settings
from django.contrib.auth.decorators import login_required


def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


#

# def search(request):
#     if not request.user.is_authenticated:
#         return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

#     else:
#         queryset = Post.objects.all()
#         query = request.GET.get('q')
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) |
#                 Q(overwiew__icontains=query)
#             ).distinct()
#     context = {
#         'queryset': queryset
#     }
#     return render(request, 'mypost/search_result.html', context)

# @login_required
# def search(request):
#     queryset = Post.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query) |
#             Q(overwiew__icontains=query)
#         ).distinct()
#     context = {
#         'queryset': queryset
#     }
#     return render(request, 'mypost/search_result.html', context)


class SearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overwiew__icontains=query) |
                Q(key_words__icontains=query)
            ).distinct()

        context = {
            'queryset': queryset,
            'query': query,
        }
        return render(request, 'mypost/search_result.html', context)


class HomeView(TemplateView):
    template_name = 'mypost/home.html'

    def get_context_data(self, **kwargs):
        post = Post.objects.all()
        context = super().get_context_data(**kwargs)

        context["post"] = post
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'mypost/create-post.html'
    context_object_name = "post"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.post_by = self.request.user
        form.save()
        return redirect(reverse("mypost:post_detail", kwargs={
            'pk': form.instance.pk
        }))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    context_object_name = "post"
    template_name = 'mypost/create-post.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.post_by = self.request.user
        form.save()
        return redirect(reverse('mypost:post_detail', kwargs={
            'pk': form.instance.pk
        }))


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = "post"
    success_url = reverse_lazy('mypost:home')
    template_name = 'mypost/detail.html'

    def get_object(self):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["post_by"] = post.post_by.username
        return context


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = "mypost/post_list.html"
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
    template_name = 'mypost/detail.html'
    context_object_name = 'post'
    form = CommentForm()

    @method_decorator(un_authenticated_user)
    def dispatch(self, * args, ** kwargs):
        return super().dispatch( * args, ** kwargs)

    def get_object(self):
        obj = super().get_object()
        self.request.session['last_view'] = obj.id
        try:
            PostView.objects.get_or_create(
                view_user=self.request.user,
                post_view=obj
            )
            
        except:
            pass
        return obj

    def get_context_data(self, **kwargs):
        most_recent = Post.objects.all().order_by('-created')[:4]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = self.get_object()
        if form.is_valid():
            form.instance.comment_by = request.user
            form.instance.for_post = post
            form.save()
        return redirect(reverse("mypost:post_detail", kwargs={
            'pk': post.pk
        }))


class CommentListView(View):
    model = Comment
    template_name = "mypost/detail.html"
    login_url = '/../../../account/login/'
    # redirect_field_name = 'next'
    context_object_name = "comment_list"

    def get_object(self):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_comment"] = self.get_object()
        return context
