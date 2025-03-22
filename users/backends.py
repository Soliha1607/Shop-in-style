from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser

class EmailBackend(ModelBackend):
    """Foydalanuvchini email orqali autentifikatsiya qiladi."""

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
