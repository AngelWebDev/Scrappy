from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import ScrappyUserManager, RightsManager


class ScrappyUser(AbstractBaseUser):
    class Meta:
        db_table = "users"

    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        PENDING = 'Pending', 'Pending'
        DEACTIVATED = 'Deactivated', 'Deactivated'

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
        ARRIVAL = 'Arrival', 'Arrival'
        PAYOUT = 'Payout', 'Payout'
        OFFICE = 'Office', 'Office'

    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)
    right = models.CharField(max_length=10, choices=RightChoices.choices)

    objects = RightsManager()


class Identification(models.Model):
    class Meta:
        db_table = "identification"

    class DocumentTypeChoices(models.TextChoices):
        IDCARD = 'IDCard', 'IDCard'
        PASSPORT = 'Passport', 'Passport'
        DRIVERLICENSE = 'Driver License', 'Driver License'

    user = models.OneToOneField(ScrappyUser, on_delete=models.SET_NULL, null=True)
    document_type = models.CharField(max_length=20, choices=DocumentTypeChoices.choices)
    document_id_number = models.CharField(max_length=255)
    name_on_document = models.CharField(max_length=255)
    issuing_country = models.CharField(max_length=255)
    document_expiration_date = models.DateField(auto_now_add=True)
    verified_at = models.DateTimeField(auto_now_add=True)


class Company(models.Model):
    class Meta:
        db_table = "company"

    name = models.CharField(max_length=255)
    vat_id = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=50)


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
    identification = models.OneToOneField(Identification, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email


class Journal(models.Model):
    class Meta:
        db_table = "journal"

    entity_name = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)
