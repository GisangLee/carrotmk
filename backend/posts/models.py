from pyexpat import model
from django.db import models
from accounts import models as user_models

# Create your models here.


class Post(models.Model):

    author = models.ForeignKey(
        user_models.User, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user_set = models.ManyToManyField(
        user_models.User, blank=True, related_name="likes_user"
    )

    def __str__(self):
        return self.title


class Photo(models.Model):
    file = models.ImageField(upload_to="posts/%Y/%m/%d")
    caption = models.TextField(blank=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return self.caption
