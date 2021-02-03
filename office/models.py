from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


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
        user.status = ScrappyUser.StatusChoices.ACTIVE
        user.save(using=self._db)
        return user


class ScrappyUser(AbstractBaseUser):
    class Meta:
        db_table = "users"

    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'active'
        PENDING = 'PENDING', 'pending'
        DEACTIVATED = 'DEACTIVATED', 'deactivated'

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    is_admin = models.BooleanField(default=False)

    objects = ScrappyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Rights(models.Model):
    class Meta:
        db_table = "rights"
        verbose_name_plural = "Rights"

    class RightChoices(models.TextChoices):
        ARRIVAL = 'ARRIVAL', 'Arrival'
        PAYOUT = 'PAYOUT', 'Payout'
        OFFICE = 'OFFICE', 'Office'

    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)
    right = models.CharField(max_length=10, choices=RightChoices.choices)


class Identification(models.Model):
    class Meta:
        db_table = "identification"

    class DocumentTypeChoices(models.TextChoices):
        IDCARD = 'IDCARD', 'IDCard'
        PASSPORT = 'PASSPORT', 'Passport'
        DRIVERLICENSE = 'DRIVERLICENSE', 'Driver License'

    user = models.OneToOneField(ScrappyUser, on_delete=models.SET_NULL, null=True)
    document_type = models.CharField(max_length=20, choices=DocumentTypeChoices.choices)
    document_id_number = models.CharField(max_length=255)
    name_on_document = models.CharField(max_length=255)
    issuing_country = models.CharField(max_length=255)
    document_expiration_date = models.DateField(auto_now_add=True)
    verified_at = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    class Meta:
        db_table = "customer"

    class TitleChoices(models.TextChoices):
        MR = 'Mr', 'Mr'
        MRS = 'Mrs', 'Mrs'
        DR = 'Dr', 'Dr'
        PROF = 'Prof', 'Prof'

    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    phone1 = models.CharField(max_length=50, null=True, blank=True)
    phone2 = models.CharField(max_length=50, null=True, blank=True)
    vat_id = models.CharField(max_length=50, null=True, blank=True)
    tax_id = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    title = models.CharField(max_length=255, choices=TitleChoices.choices, default=TitleChoices.MR)
    status = models.BooleanField(default=True)
    identification = models.OneToOneField(Identification, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.email


class Journal(models.Model):
    class Meta:
        db_table = "journal"

    entity_name = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)
