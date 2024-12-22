from decimal import Decimal

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from .constants import GENDER_CHOICE
from .managers import UserManager

# from decimal import Decimal

# from django.contrib.auth.models import AbstractUser
# from django.core.validators import (
#     MinValueValidator,
#     MaxValueValidator,
# )
# from django.db import models

# from .constants import GENDER_CHOICE

# from .managers import UserManager

# from django.conf import settings


# from django.utils import timezone

# ##

# from django.contrib.auth.models import AbstractUser

# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .managers import UserManager

# from decimal import Decimal
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.db import models
# from django.utils import timezone
# from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def balance(self):
        # Calculate the total balance from all linked bank accounts
        total_balance = sum(account.balance for account in self.bank_accounts.all())
        return total_balance

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(decimal_places=2, max_digits=12)
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='The number of times interest will be calculated per year'
    )

    def __str__(self):
        return self.name

    def calculate_interest(self, principal):
        """
        Calculate interest for each account type.

        This uses a basic interest calculation formula
        """
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)

        # Basic Future Value formula to calculate interest
        interest = (p * (1 + ((r/100) / n))) - p

        return round(interest, 2)


class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text='The month number that interest calculation will start from'
    )
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.account_no)

    def get_interest_calculation_months(self):
        """
        List of month numbers for which the interest will be calculated

        returns [2, 4, 6, 8, 10, 12] for every 2 months interval
        """
        interval = int(
            12 / self.account_type.interest_calculation_per_year
        )
        start = self.interest_start_date.month
        return [i for i in range(start, 13, interval)]


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email


# from django.db import models
# from django.conf import settings

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Profile')
#     account_type = models.CharField(max_length=20, blank=True)
#     gender = models.CharField(max_length=10, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     # street_address = models.CharField(max_length=255, blank=True)
#     # city = models.CharField(max_length=100, blank=True)
#     # postal_code = models.CharField(max_length=20, blank=True)
#     # country = models.CharField(max_length=100, blank=True)
#     image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
#     info = models.CharField(max_length=100, blank=True)
#     social = models.CharField(max_length=100, blank=True)
#     connection = models.CharField(max_length=100, blank=True)
#     notification = models.CharField(max_length=100, blank=True)
    
#     def __str__(self):
#          return f'{self.user.username} Profile'





# accounts/models.py

###########################

#prevent user login 
from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:  # Check if user is active
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
