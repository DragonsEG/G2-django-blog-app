from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    contacts = ArrayField(PhoneNumberField(max_length=20,null=True,blank=True),size=4)
    social_link1 = models.URLField(max_length=100,null=True,blank=True)
    social_link2 = models.URLField(max_length=100,null=True,blank=True)
    admin = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='company_admin',null=True)

    def __str__(self) -> str:
        return self.company_name


def user_images(obj,filename):
    return f'images/profils/{obj.user.username}/{filename}'

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='profile')
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=user_images,null=True)
    badge = models.ImageField(upload_to=user_images,null=True)
    company = models.ForeignKey(CompanyProfile,on_delete=models.SET_NULL,related_name='company',null=True)
    link1 = models.URLField(max_length=100,null=True,blank=True)
    link2 = models.URLField(max_length=100,null=True,blank=True)


    def __str__(self) -> str:
        return self.user.username





class PublishedManger(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset() \
                    .filter(status=Post.Status.PUBLISHED)








class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft' 
        PUBLISHED = 'PB', 'Published'

    tags = TaggableManager()

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')


    objects = models.Manager()
    published = PublishedManger()




    class Meta: 
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]



    def __str__(self) -> str:
        return self.title
    

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'



