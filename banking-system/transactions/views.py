from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
##
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
##
from transactions.constants import DEPOSIT, TRANSFER, WITHDRAWAL, PAYMENT
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm, 
)
from .forms import FDApplicationForm, RDApplicationForm
from transactions.models import Transaction, FDApplication, RDApplication
from accounts.models import UserBankAccount

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from accounts.models import Profile, UserAddress, UserBankAccount
# from .forms import ProfileUpdateForm
from core.decorators import admin_required

class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money to Your Account'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = (
                now + relativedelta(
                    months=+next_interest_month
                )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )

        messages.success(
            self.request,
            f'Rs.{amount} was deposited to your account successfully'
        )

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'deposit'
        return context


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn Rs.{amount} from your account'
        )

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'withdraw'
        return context

####

# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from accounts.forms import UserAddressForm
from .forms import CustomPasswordChangeForm
# from accounts.models import Profile, UserAddress
# from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect

@login_required
def profile(request):
    user = request.user
    # profile, created = Profile.objects.get_or_create(user=user)
    # address, created = UserAddress.objects.get_or_create(user=user)
    # profile_form = ProfileUpdateForm(instance=profile)
    # address_form = UserAddressForm(instance=address)
    password_change_form = CustomPasswordChangeForm(user=user)
    
    if request.method == 'POST':
        # print("Form submission received:", request.POST)
        if 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            password_change_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_change_form.is_valid():
                password_change_form.save()
                update_session_auth_hash(request, request.user)  # Important to keep the user logged in
                # print("Password changed successfully!")
                messages.success(request, 'Your password was successfully updated!')
                return redirect('transactions:profile')
            else:
                # print("Form errors:", password_change_form.errors)
                # print("Form data:", request.POST)
                return redirect('transactions:profile')
        # else:
        #     print("test")
            # Handle profile and address update
            # profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            # address_form = UserAddressForm(request.POST, instance=address)
            # if profile_form.is_valid() and address_form.is_valid():
            #     profile_form.save()
            #     address_form.save()
            #     messages.success(request, 'Profile details updated successfully.')
            #     return redirect('transactions:profile')
            # else:
            #     print("Profile form errors:", profile_form.errors)
            #     print("Address form errors:", address_form.errors)

    context = {
        'user': user,
        'profile': profile,
        # 'profile_form': profile_form,
        # 'address_form': address_form,
        'password_change_form': password_change_form,
    }
    return render(request, 'transactions/profile.html', context)



# class ChangePasswordView(PasswordChangeView):
#     form_class=PasswordChangeForm
#     success_url='transactions/profile/'
    

# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important to update the session with new auth hash
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('transactions:profile')  # Redirect to profile or any other page
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
    
#     return render(request, 'transactions/profile.html', {'form': form})






##transact start
@login_required
def transact(request):
        return render(request, 'transactions/transact.html')
@login_required
def fd_rd(request):
        return render(request, 'transactions/fd_rd.html')
@login_required
def check_status(request):
        return render(request, 'transactions/check_status.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PaymentForm, TransferForm

# @login_required
# def payment_view(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             Payment.objects.create(
#                 recipient_name=form.cleaned_data['recipient_name'],
#                 recipient_account=form.cleaned_data['recipient_account'],
#                 amount=form.cleaned_data['amount'],
#                 payment_method=form.cleaned_data['payment_method'],
#                 description=form.cleaned_data['description'],
#             )
#             messages.success(request, 'Payment successful!')
#             return redirect('transactions:payment_form')
#         else:
#             messages.error(request, 'There was an error with your submission.')
#     else:
#         form = PaymentForm()

#     return render(request, 'transactions/payment_form.html', {'form': form})

# @login_required
# def transfer_view(request):
#     def get_initial():
#         return {'transaction_type': TRANSFER}

#     if request.method == 'POST':
        
#         form = TransferForm(request.POST, user=request.user)
#         if form.is_valid():
#             # Create Transfer object (assuming Transfer model exists)
#             transfer = form.save(commit=False)
#             transfer.save()

#             # Update user's account balance
#             request.user.account.balance -= form.cleaned_data['amount']
#             request.user.account.save(update_fields=['balance'])

#             messages.success(request, f'Successfully transferred Rs.{form.cleaned_data["amount"]} from your account')
#             return redirect('transactions:transfer_form')  # Redirect to the same form or another URL
#         else:
#             messages.error(request, 'There was an error with your submission.')
#     else:
#         form = TransferForm(user=request.user, initial=get_initial())

#     return render(request, 'transactions/transfer_form.html', {'form': form})


# views.py
# views.py


# Assuming you have defined this mixin

# views.py

# views.py

class PaymentView(TransactionCreateMixin):
    form_class = PaymentForm
    title = 'PAYMENT'

    def get_initial(self):
        initial = {'transaction_type': PAYMENT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        recipient_account_no = form.cleaned_data.get('recipient_account')

        # Update the user's account balance
        user_account = self.request.user.account
        user_account.balance -= amount
        user_account.save(update_fields=['balance'])

        # # Create transaction for the user's account
        # user_transaction = Transaction.objects.create(
        #     account=user_account,
        #     amount=amount,
        #     transaction_type=PAYMENT,
        #     description=form.cleaned_data.get('description'),
        #     recipient_name=form.cleaned_data.get('recipient_name'),
        #     recipient_account=recipient_account_no,
        #     payment_method=form.cleaned_data.get('payment_method'),
        #     balance_after_transaction=user_account.balance
        # )

        # Update recipient's account balance and create transaction if it exists
        recipient_account = UserBankAccount.objects.get(account_no=recipient_account_no)
        recipient_account.balance += amount
        recipient_account.save(update_fields=['balance'])

        recipient_transaction = Transaction.objects.create(
            account=recipient_account,
            amount=amount,
            transaction_type=PAYMENT,
            description=f'Received payment from {self.request.user.first_name}',
            balance_after_transaction=recipient_account.balance
        )

        messages.success(
            self.request,
            f'Successfully PAID Rs.{amount} to account number {recipient_account_no}'
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'payment'
        return context
    
class TransferView(TransactionCreateMixin):
    form_class = TransferForm
    title = 'TRANSFER'

    def get_initial(self):
        initial = {'transaction_type': TRANSFER}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        source_account = self.request.user.account
        destination_account_number = form.cleaned_data.get('destination_account')

        # Deduct amount from source account
        source_account.balance -= amount
        source_account.save(update_fields=['balance'])

        # Add amount to destination account
        try:
            destination_account = UserBankAccount.objects.get(account_no=destination_account_number)
            destination_account.balance += amount
            destination_account.save(update_fields=['balance'])
        except UserBankAccount.DoesNotExist:
            form.add_error('destination_account', 'Destination account does not exist.')
            return self.form_invalid(form)

        # # Create a transaction record for the source account
        # Transaction.objects.create(
        #     account=source_account,
        #     amount=amount,
        #     balance_after_transaction=source_account.balance,
        #     transaction_type=TRANSFER,
        #     source_account=source_account.account_no,
        #     destination_account=destination_account_number,
        #     description=form.cleaned_data.get('description')
        # )

        # Create a transaction record for the destination account
        Transaction.objects.create(
            account=destination_account,
            amount=amount,
            balance_after_transaction=destination_account.balance,
            transaction_type=TRANSFER,
            source_account=source_account.account_no,
            destination_account=destination_account_number,
            description=form.cleaned_data.get('description')
        )

        messages.success(
            self.request,
            f'Successfully TRANSFERRED Rs.{amount} from your account to account {destination_account_number}'
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'transfer'
        return context



#FD and RD

@login_required
def apply_fd(request):
    if request.method == 'POST':
        form = FDApplicationForm(request.POST)
        if form.is_valid():
            fd_application = form.save(commit=False)
            fd_application.user = request.user
            fd_application.save()
            return redirect('transactions:application_success')
    else:
        form = FDApplicationForm()
    return render(request, 'transactions/apply_fd.html', {'form': form})

@login_required
def apply_rd(request):
    if request.method == 'POST':
        form = RDApplicationForm(request.POST)
        if form.is_valid():
            rd_application = form.save(commit=False)
            rd_application.user = request.user
            rd_application.save()
            return redirect('transactions:application_success')
    else:
        form = RDApplicationForm()
    return render(request, 'transactions/apply_rd.html', {'form': form})

@login_required
def user_fd_applications(request):
    fd_applications = FDApplication.objects.filter(user=request.user)
    return render(request, 'transactions/user_fd_applications.html', {'fd_applications': fd_applications})

@login_required
def user_rd_applications(request):
    rd_applications = RDApplication.objects.filter(user=request.user)
    return render(request, 'transactions/user_rd_applications.html', {'rd_applications': rd_applications})

@login_required
def application_success(request):
    return render(request, 'transactions/application_success.html')

@login_required
@admin_required
def approve_fd_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(FDApplication, id=application_id)
        application.status = 'Approved'
        application.save()
    return redirect('core:fd_rd_request')

@login_required
@admin_required
def reject_fd_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(FDApplication, id=application_id)
        application.status = 'Rejected'
        application.save()
    return redirect('core:fd_rd_request')

@login_required
@admin_required
def approve_rd_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(RDApplication, id=application_id)
        application.status = 'Approved'
        application.save()
    return redirect('core:fd_rd_request')

@login_required
@admin_required
def reject_rd_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(RDApplication, id=application_id)
        application.status = 'Rejected'
        application.save()
    return redirect('core:fd_rd_request')



# View to handle deletion of FD Application
def delete_fd_application(request, application_id):
    application = get_object_or_404(FDApplication, id=application_id)
    application.delete()
    messages.success(request, 'FD Application has been successfully deleted.')
    return redirect('core:fd_rd_request')  # Adjust the redirect URL as needed

# View to handle deletion of RD Application
def delete_rd_application(request, application_id):
    application = get_object_or_404(RDApplication, id=application_id)
    application.delete()
    messages.success(request, 'RD Application has been successfully deleted.')
    return redirect('core:fd_rd_request')  # Adjust the redirect URL as needed

