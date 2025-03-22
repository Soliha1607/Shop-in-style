from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Email orqali autentifikatsiya qilish uchun CustomUserManager."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart!")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Parolni hash qilish
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo‘lishi shart!")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo‘lishi shart!")

        return self.create_user(email, password, **extra_fields)
