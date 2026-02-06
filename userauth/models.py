from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # You can add additional fields here if needed
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150, unique=False,null=True,blank=True)
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        email_username , _ = self.email.split('@')
        if self.username is None or self.username == "":
           self.username = email_username
           
        super(User,self).save(*args, **kwargs)
        


    
     
