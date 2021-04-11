import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.sites.models import Site
from django.contrib.auth.models import AbstractBaseUser

from invitations import signals
from invitations.app_settings import app_settings
from invitations.base_invitation import AbstractBaseInvitation
from invitations.adapters import get_invitations_adapter

from .managers import ScrappyUserManager, RightsManager


class ScrappyUser(AbstractBaseUser):
    class Meta:
        db_table = "users"

    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        PENDING = 'Pending', 'Pending'
        DEACTIVATED = 'Deactivated', 'Deactivated'

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
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


class Company(models.Model):
    class Meta:
        db_table = "company"
        verbose_name_plural = "Companies"

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
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    title = models.CharField(max_length=255, choices=TitleChoices.choices, default=TitleChoices.MR)
    comments = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.firstname.capitalize(), self.lastname.capitalize())


class Identification(models.Model):
    class Meta:
        db_table = "identification"

    class DocumentTypeChoices(models.TextChoices):
        IDCARD = 'IDCard', 'IDCard'
        PASSPORT = 'Passport', 'Passport'
        DRIVERLICENSE = 'Driver License', 'Driver License'

    user = models.ForeignKey(ScrappyUser, on_delete=models.SET_NULL, null=True)
    document_type = models.CharField(max_length=20, choices=DocumentTypeChoices.choices)
    document_id_number = models.CharField(max_length=255)
    name_on_document = models.CharField(max_length=255)
    issuing_country = models.CharField(max_length=255)
    document_expiration_date = models.DateField(null=True, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='identifications')


class Journal(models.Model):
    class Meta:
        db_table = "journal"

    entity_name = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)


class CustomInvitation(AbstractBaseInvitation):
    class Meta:
        db_table = "invitation"

    email = models.EmailField(unique=True, max_length=255)
    created = models.DateTimeField(default=timezone.now)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    arrival = models.BooleanField(default=False)
    payout = models.BooleanField(default=False)
    office = models.BooleanField(default=False)

    @classmethod
    def create(cls, email, firstname, lastname, inviter=None, **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.filter(email=email).first()
        if instance:
            instance.delete()

        new_instance = cls._default_manager.create(
            email=email,
            firstname=firstname,
            lastname=lastname,
            key=key,
            inviter=inviter,
            **kwargs)
        return new_instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = kwargs.pop('site', Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update({
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
        })

        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter)

    def __str__(self):
        return "Invite: {0}".format(self.email)