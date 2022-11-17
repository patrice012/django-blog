
from django.urls import path

from profilapp.views import (
    profil,
    # ProfileCreateView,
    ProfileUpdateView,
    ProfileDetailView,
)


app_name = 'profilapp'
urlpatterns = [
    # path('create/', ProfileCreateView.as_view(), name='create_profile'),
    
    path('update/<pk>/', ProfileUpdateView.as_view(), name='update_profile'),
    path('<pk>/', ProfileDetailView.as_view(), name="profile"),
    
]