from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.urls import reverse
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save

import os

from utils.models import UrlMixin, TimeStampedModel

User = settings.AUTH_USER_MODEL

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name  




# SEXE = (
#     ('M', 'masculin'),
#     ('F','Feminin')
# )

# CONTINENT = (
#     ('AF','AFRIQUE'),
#     ('UE', 'EUROPE'),
#     ('AM', 'AMERIQUE'),
#     ('AS', 'ASIE'),
#     ('OC','OCEANIE'),
# )

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now =True)

    class Meta:
        abstract = True

# class profilMixin(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(User, verbose_name="Auteur", on_delete=models.CASCADE)
#     name = models.CharField( max_length=20 , verbose_name = 'Nom de profil')
#     email = models.EmailField(max_length=254, verbose_name = ' E-mail')

#     class Meta:
#         abstract = True


# Create your models here.
class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True, null = False, editable=False)
    email = models.EmailField(max_length=254, verbose_name = ' E-mail')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    proffession = models.CharField(max_length=50)
    tel = models.IntegerField(null = True, blank = True, verbose_name = 'Numero de Téléphone')
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250

        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username

    def get_profil_url(self):
            return reverse('profilapp:profile', kwargs = {
                'pk': self.id
            })


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)





# class AuthorProfil(profilMixin, TimeStampedModel):
#     tel = models.IntegerField(verbose_name = 'Numero de Téléphone')
#     sexe = models.CharField(choices = SEXE, max_length = 1)
#     proffession = models.CharField(max_length=50)
#     experience = models.IntegerField(verbose_name = 'Année d\'experince')
#     pays = models.CharField(max_length=30)
#     continent = models.CharField(choices = CONTINENT, max_length=50)
#     profil_picture = models.ImageField(upload_to='AuthorPicture',max_length=1200, verbose_name = 'photo de profile', null = True, blank = True)

#     def __str__(self):
#         return self.name

#     def get_profil_url(self):
#             return reverse('profilapp:profil', kwargs = {
#                 'uuid': self.id
#             })

# class ReaderProfil(profilMixin, TimeStampedModel):
#     profil_picture = models.ImageField(upload_to='ReaderPicture',max_length=1200, verbose_name = 'photo de profile', null = True, blank = True)

#     def __str__(self):
#             return self.name

#     def get_profil_url(self):
#             return reverse('profilapp:profil', kwargs = {
#                 'uuid': self.id
#             })
