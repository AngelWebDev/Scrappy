from django.db.models import Manager as BaseManager
from django.contrib.auth.models import BaseUserManager


class ScrappyUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
        user.is_admin = True
        user.status = self.model.StatusChoices.ACTIVE
        user.save(using=self._db)
        return user


class RightsManager(BaseManager):
    def update_rights(self, user, **kwargs):
        for right_name in kwargs.keys():
            existing_right = self.model.objects.filter(user=user, right=right_name)
            if kwargs[right_name]:
                if not existing_right:
                    new_right = self.model()
                    new_right.right = right_name
                    new_right.user = user
                    new_right.save(using=self._db)
            else:
                if existing_right:
                    existing_right.delete()
        return True
