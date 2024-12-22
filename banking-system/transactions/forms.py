import datetime

from django import forms
from django.conf import settings

from .models import Transaction, FDApplication, RDApplication

from django import forms
from accounts.models import UserBankAccount  # Corrected import
from django.core.exceptions import ValidationError

from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import User

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['account_type', 'gender', 'birth_date', 'image', 'info', 'social', 'connection', 'notification']

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type',
            'source_account',
            'destination_account',
            'description',
            'recipient_name',
            'recipient_account',
            'payment_method',
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        # Disable transaction_type field and hide it
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        # Set account and balance_after_transaction
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance

        # Call parent save method
        return super().save(commit=commit)

class DepositForm(TransactionForm):

    def clean_amount(self):
        min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
        amount = self.cleaned_data.get('amount')

        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} Rupees'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT
        max_withdraw_amount = (
            account.account_type.maximum_withdrawal_amount
        )
        balance = account.balance

        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} Rupees'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} Rupees'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'You have Rs. {balance} in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount


class TransactionDateRangeForm(forms.Form):
    daterange = forms.CharField(required=False)

    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")
        print(daterange)

        try:
            daterange = daterange.split(' - ')
            print(daterange)
            if len(daterange) == 2:
                for date in daterange:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                return daterange
            else:
                raise forms.ValidationError("Please select a date range.")
        except (ValueError, AttributeError):
            raise forms.ValidationError("Invalid date range")




# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['account_type', 'gender', 'birth_date', 'image', 'info', 'social', 'connection', 'notification']    
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['account_type'].widget.attrs['readonly'] = True
#         self.fields['gender'].widget.attrs['readonly'] = True
#         self.fields['birth_date'].widget.attrs['readonly'] = True



class CustomPasswordChangeForm(PasswordChangeForm):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('current_password', 'new_password1', 'new_password2')

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not check_password(current_password, self.user.password):
            raise forms.ValidationError('Current password is incorrect')
        return current_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('New passwords do not match')
        return new_password2

    def save(self, commit=True):
        user = self.user
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        self._errors.pop('old_password', None)  # Remove any old password errors
        return cleaned_data

class PaymentForm(TransactionForm):
    recipient_name = forms.CharField(max_length=100, label='Recipient Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipient_account = forms.CharField(max_length=100, label='Recipient Account', widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label='Amount', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('bank_account', 'Bank Account')
    ], label='Payment Method', widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT
        max_withdraw_amount = account.account_type.maximum_withdrawal_amount
        balance = account.balance

        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You have to Pay at least {min_withdraw_amount} Rupees'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can Pay at most {max_withdraw_amount} Rupees'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'You have Rs. {balance} in your account. '
                'You can not Pay more than your account balance'
            )

        return amount

    def clean_recipient_account(self):
        recipient_account_no = self.cleaned_data.get('recipient_account')
        user_account = str(self.account.account_no)   

        # Check if the recipient account is the same as the user's account
        if recipient_account_no == user_account:
            raise ValidationError('You cannot make a payment to your own account.')

        
        if not UserBankAccount.objects.filter(account_no=recipient_account_no).exists():
            raise forms.ValidationError('The recipient account number does not exist.')

        return recipient_account_no


class TransferForm(TransactionForm):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    source_account = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    destination_account = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    def clean_amount(self):
        account = self.account
        min_transfer_amount = settings.MINIMUM_TRANSFER_AMOUNT
        max_transfer_amount = account.account_type.maximum_withdrawal_amount
        balance = account.balance

        amount = self.cleaned_data.get('amount')

        if amount < min_transfer_amount:
            raise forms.ValidationError(
                f'You must transfer at least {min_transfer_amount} Rupees'
            )

        if amount > max_transfer_amount:
            raise forms.ValidationError(
                f'You cannot transfer more than {max_transfer_amount} Rupees'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'You have Rs. {balance} in your account. '
                'You cannot transfer more than your account balance.'
            )

        return amount

    def clean(self):
        cleaned_data = super().clean()
        source_account_number = cleaned_data.get('source_account')
        destination_account_number = cleaned_data.get('destination_account')

        # Validate source and destination accounts
        if source_account_number == destination_account_number:
            raise ValidationError('Source and destination accounts cannot be the same.')

        try:
            source_account = UserBankAccount.objects.get(account_no=source_account_number)
        except UserBankAccount.DoesNotExist:
            raise ValidationError('Source account does not exist.')

        if source_account != self.account:
            raise ValidationError('Source account must be your own account.')

        try:
            destination_account = UserBankAccount.objects.get(account_no=destination_account_number)
        except UserBankAccount.DoesNotExist:
            raise ValidationError('Destination account does not exist.')

        return cleaned_data

    def save(self, commit=True):
        # Optionally override save method if additional logic is needed
        return super().save(commit=commit)


##FD and RD

class FDApplicationForm(forms.ModelForm):
    class Meta:
        model = FDApplication
        fields = ['amount', 'tenure', 'interest_rate']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenure': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("The amount must be a positive number.")
        return amount

    def clean_tenure(self):
        tenure = self.cleaned_data.get('tenure')
        if tenure is not None and tenure <= 0:
            raise ValidationError("The tenure must be a positive number.")
        return tenure

    def clean_interest_rate(self):
        interest_rate = self.cleaned_data.get('interest_rate')
        if interest_rate is not None and interest_rate <= 0:
            raise ValidationError("The interest rate must be a positive number.")
        return interest_rate
    
class RDApplicationForm(forms.ModelForm):
    class Meta:
        model = RDApplication
        fields = ['amount', 'monthly_amount', 'tenure', 'interest_rate']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'tenure': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("The amount must be a positive number.")
        return amount

    def clean_monthly_amount(self):
        monthly_amount = self.cleaned_data.get('monthly_amount')
        if monthly_amount is not None and monthly_amount <= 0:
            raise ValidationError("The monthly amount must be a positive number.")
        return monthly_amount

    def clean_tenure(self):
        tenure = self.cleaned_data.get('tenure')
        if tenure is not None and tenure <= 0:
            raise ValidationError("The tenure must be a positive number.")
        return tenure

    def clean_interest_rate(self):
        interest_rate = self.cleaned_data.get('interest_rate')
        if interest_rate is not None and interest_rate <= 0:
            raise ValidationError("The interest rate must be a positive number.")
        return interest_rate
