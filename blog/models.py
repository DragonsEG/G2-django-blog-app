from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Post (models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft' 
        PUBLISHED = 'PB', 'Published'

    class Category(models.TextChoices):
        NEWS = 'News','News'
        TUTORIAL = 'Tutorial','Tutorial'
        BUSINESS = 'Business','Business'

    title = models.CharField(max_length=255)
    statue = models.CharField(max_length=2,choices=Status.choices)
    categories = models.CharField(max_length=10,choices=Category.choices)
    content = HTMLField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts_owner'
    )
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Comment (models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    comment_content = models.CharField(max_length=255)
    publish_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

class company (models.Model) :
    name = models.CharField(max_length=255) 
    mail = models.EmailField()

class CompanyWriters (models.Model) :
    company = models.ForeignKey(
        company , 
        on_delete= models.CASCADE 
    )
    Writer = models.ForeignKey(
        User , 
        on_delete=models.CASCADE 
    )

# Create your models here.
