from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth import get_user_model
# CCreate a User manager to manage the User objects
class UserManager(BaseUserManager):

    #creates a user with email and password, raises error when email is not provided
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        extra_fields.setdefault('username', email)
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #create a super user by calling the create_user function and making the user active,staff,super_user and saving the user
    def create_superuser(self,email,password):
        user=self.create_user(email=email,password=password)
        user.is_active = True
        user.is_staff =True
        user.is_superuser=True
        user.save(using=self._db)
        return user

#create a custom user model subclassing the AbstractUser
    
class CustomUser(AbstractUser):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    objects = UserManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]

class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='following')
    following=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='followers')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['follower','following'],name='unique_following')
        ]
    
    def __str__(self):
        return f"{self.follower} follows {self.following} "

