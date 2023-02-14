from django.contrib.auth.base_user import BaseUserManager

from .constants import IS_STAFF, IS_SUPERUSER


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique and required parameter.
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.clean()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault(IS_STAFF, False)
        extra_fields.setdefault(IS_SUPERUSER, False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault(IS_STAFF, True)
        extra_fields.setdefault(IS_SUPERUSER, True)

        if extra_fields.get(IS_STAFF) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get(IS_SUPERUSER) is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
