from django.contrib.auth.models import BaseUserManager as DefaultManager


class BaseUserManager(DefaultManager):

    def create_user(self, email, password=None, *args, **kwargs):

        if email is None:
            raise TypeError('Пользователь должен иметь email')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, *args, **kwargs):

        if password is None:
            raise TypeError('Cуперпользователя должен иметь пароль')

        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
