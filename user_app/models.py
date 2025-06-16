from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime
import os

# Create your models here.
class User(AbstractUser):
    is_teacher= models.BooleanField('Is teacher', default=False)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    desc = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
