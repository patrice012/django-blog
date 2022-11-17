from django.db import models
from django.urls import reverse

from utils.models import UrlMixin, TimeStampedModel
from post import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class PostView(models.Model):
    post_view = models.ForeignKey('Post', on_delete=models.CASCADE)
    view_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(TimeStampedModel):
    for_post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, verbose_name="Commenter par", on_delete=models.CASCADE)
    comment_body = models.TextField(verbose_name="Votre commentaire")

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.comment_by.username


class Post(TimeStampedModel):
    post_by = models.ForeignKey(User, verbose_name="Auteur", on_delete=models.CASCADE)
    title = models.CharField(max_length=60, verbose_name="Titre")
    overwiew = models.CharField(max_length=20, verbose_name="Bref appercu du post", )
    key_words = models.CharField(max_length=20, verbose_name='Mots clés...  Facultatif', null=True, blank='True')
    content = models.TextField(verbose_name="Contenu du post")
    post_image = models.ImageField(upload_to="media", verbose_name="Associer une image")
    previous_post = models.ForeignKey('self', related_name='previous', null=True, blank=True, on_delete=models.SET_NULL)
    next_post = models.ForeignKey('self', related_name='next', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mypost:post_detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('mypost:post_update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('mypost:post_delete', kwargs={
            'pk': self.pk
        })

    def get_comment_url(self):
        return reverse('mypost:comment_post', kwargs={
            'pk': self.pk
        })

    @property
    def view_count(self):
        return PostView.objects.filter(post_view=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(for_post=self).count()

    @property
    def get_comments(self):
        return self.comments.all().order_by('-created')
