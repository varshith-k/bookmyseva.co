from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,fullname=None,mobile_number=None,address=None,city=None,main_service=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            mobile_number=mobile_number,
            address=address,
            city=city,
            main_service=main_service,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,fullname,mobile_number,address,city,main_service):
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
            mobile_number=mobile_number,
            address=address,
            city=city,
            main_service=main_service,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(max_length=50)
    mobile_number = models.IntegerField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    main_service = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname','mobile_number','address','city','main_service']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
