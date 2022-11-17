from django.urls import path

from . import views

from .views import (
    SearchView,
    CommentListView,
    HomeView,
    CreatePostView,
    PostListView,
    PostUpdateView,
    PostDetailView,
    PostDeleteView,
)

app_name = 'mypost'
urlpatterns = [
    path('', HomeView.as_view(), name ='home'),
    path('post-create/', CreatePostView.as_view(), name='post_create'),
    path('post-list/', PostListView.as_view(), name='post_list'),
    path('post-update/<int:pk>/',PostUpdateView.as_view(), name='post_update' ),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name ='post_detail'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name ='post_delete'),

    # path('post-detail/<int:pk>/comment/', CommentView.as_view(), name='comment_post' ),
    path('post-detail/<int:pk>/comment-list/', CommentListView.as_view(), name='comment_post' ),
    path('search/', SearchView.as_view(), name='search_post' ),
    
    # path('search/', views.search, name='search_post'),


    
]