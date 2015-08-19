from django.db import models

from django.utils import timezone
from django.core import validators
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser # hashed passwords, tokenized password resets
from django.contrib.auth.models import BaseUserManager

class User(AbstractBaseUser):
    """
    A custom User model tailored for SEMP
    """
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })"""
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=50)
    last_name = models.CharField(_('last_name'), max_length=50)
    
    POSITIONS = (
        ('LTA', 'LTA'),
        ('RTA', 'RTA'),
        ('MTA', 'MTA'),
        ('CONS', 'Consultant'),
        ('SERVER', 'Server'),
        ('KIT', 'Kitchen'),
        ('SECR', 'Security'),
        ('MD', 'MD'),
    )

    STATUS = (
        ('RGLR', 'Regular'),
        ('LEAD', 'Lead'),
        ('SPV', 'Supervisor'),
    )

    position = models.CharField(_('Position'), max_length=10, choices=POSITIONS)
    status = models.CharField("Status", max_length=10, choices=STATUS)
    is_staff = models.BooleanField()
    
    USERNAME_FIELD = 'username' # Use email as username.
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'position', 'status']

    class Meta:
        db_table = 'auth_user' # Use the table auth_user.
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

"""
class BaseUserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        
        Normalize the address by lowercasing the domain part of the email
        address.
        
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
"""
class UserManager(BaseUserManager):
    """
    A custom User manager for SEMP
    """
    use_in_migrations = True # Make UserManager available in RunPython operations.

    def _create_user(self, username, email, first_name, last_name, position, status, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given information.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        if not email:
            raise ValueError('The email must be set')
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          position=position, status=status, is_staff=is_staff,
                          is_active=False, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, position, status, password=None, **extra_fields):
        return self._create_user(username, email, first_name, last_name, position, status, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, first_name, last_name, position, status, password, **extra_fields):
        return self._create_user(username, email, first_name, last_name, position, status, password, True, True,
                                 **extra_fields)