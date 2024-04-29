from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, logging, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            logging=logging
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, logging, password=None):
        user = self.create_user(
            email=email,
            logging=logging,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True  # Установка is_staff в True для суперпользователя
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    logging = models.CharField(max_length=35, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Добавленный атрибут is_staff

    objects = CustomUserManager()

    USERNAME_FIELD = 'logging'
    REQUIRED_FIELDS = ['email']

    def str(self):
        return self.logging

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def delete(self, *args, **kwargs):
        # Проверяем, существует ли пользователь
        if self.pk:
            # Удаляем все посты, связанные с этим пользователем
            Post.objects.filter(author=self).delete()
        # Вызываем стандартный метод delete
        return super().delete(*args, **kwargs)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    descriptor = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    photo = models.ImageField(blank=True, upload_to='user_image', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'Post by {self.author.username}'