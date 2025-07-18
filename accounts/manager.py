from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set. Don't miss it"))
        email = self.normalize_email(email)
        role = extra_fields.pop("role", "User")
        user = self.model(email=email, role=role, **extra_fields)
        user.is_active = True

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError(_("Superuser must have a password"))

        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.role = "Admin"
        user.save(using=self._db)
        return user
