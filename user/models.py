from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # email로 회원가입
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # profile_img = models.ImageField()
    # profile_song = models.CharField(max_length=100)   # music 테이블과 one to one 으로 수정될예정

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    # custom 유저모델을 기본 유저모델로 사용하기 위한 필수코드
    def has_perm(self, perm, obj=None): # 권한이 있는지
        return True

    def has_module_perms(self, app_label):  # App의 모델에 접근가능 하도록 
        return True

    @property
    def is_staff(self): # 관리자 화면에 접근하도록
        return self.is_admin
