from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from PIL import Image




class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=12,blank=True)
    image = models.ImageField(upload_to='profile_pictures', default='default.png')
    description = models.CharField(max_length=100,blank=True,null=True)
    # date_joined = models.DateField(auto_now_add=True)
    # last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'

    # to size the image during upload we override the save method of modelform

    # def save(self,*args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path) # here 'Image' is the imported module/method from PIL(pillow)
    #
    #     if img.height > 300 or img.width > 300:    # 300px is the size we wanted
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

class Post(models.Model):

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True)
    objects = models.Manager()
    comments = models.Manager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('blogapp:post_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):

    post = models.ForeignKey('blogapp.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField(max_length=264)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blogapp:post_list')

    def __str__(self):
        return self.text
