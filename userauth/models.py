from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):

    def create_user(self, fullname, email, is_ideator, is_IC, is_IG_admin, password):
        if not email:
            raise ValueError("User must have an email.")
        user = self.model(
            fullname = fullname,
            email = email,
            is_ideator = is_ideator,
            is_IC = is_IC,
            is_IG_admin = is_IG_admin,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, is_ideator, is_IC, is_IG_admin, password):
        user = self.create_user(
            fullname = fullname,
            email = email,
            is_ideator = is_ideator,
            is_IC = is_IC,
            is_IG_admin = is_IG_admin,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class Account(AbstractBaseUser):
    email           = models.EmailField(max_length=50, unique =True)
    fullname        = models.CharField(max_length=20)
    is_ideator      = models.BooleanField(default=False)
    is_IC           = models.BooleanField(default=False)
    is_IG_admin     = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'is_ideator', 'is_IC', 'is_IG_admin']

    def __str__(self):
        return self.fullname
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True