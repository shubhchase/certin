import random
import string
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from flask_login import login_required
from django.contrib.auth.hashers import make_password
from .forms import ForgotPasswordForm, UserRegistrationForm, UserAddressForm, UserLoginForm
from transactions.forms import CustomPasswordChangeForm
from django.contrib.auth import login as auth_login
User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            auth_login(request, user, backend='accounts.models.CustomAuthBackend')
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)

###


# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
from django.views import View
# from .forms import UserLoginForm
# import random

def generate_captcha():
    return str(random.randint(100000, 999999))

def set_captcha_session(request):
    captcha = generate_captcha()
    request.session['captcha'] = captcha

class UserLoginView(View):
    #only unauthenticated user can access login page after authentication
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:  # Check if the user is an admin
                return redirect('core:adminpanel')  
            return redirect('transactions:profile')  
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request):
        form = UserLoginForm()
        set_captcha_session(request)
        return render(request, 'accounts/user_login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            entered_captcha = form.cleaned_data['captcha']
            
            # Validate captcha
            if entered_captcha == request.session.get('captcha'):
                # Clear captcha session
                del request.session['captcha']
                
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser:  # Check if the user is an admin
                        return redirect('core:adminpanel')  
                    return redirect('transactions:profile') 
                else:
                    form.add_error(None, 'Invalid username or password.')
            else:
                form.add_error('captcha', 'Incorrect captcha.')
        
        return render(request, 'accounts/user_login.html', {'form': form})
####


class LogoutView(RedirectView):
    pattern_name = 'core:index'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

from django.contrib.auth.hashers import check_password

def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            user = request.user
            if check_password(current_password, user.password):
                # Password is correct, so update the password
                user.set_password(new_password1)
                user.save()
                return HttpResponseRedirect('/success/')
            else:
                # Password is incorrect, so show an error message
                raise Http404("Page not found")
    else:
        form = CustomPasswordChangeForm()
    return render(request, 'transactions/profile.html', {'form': form})



##update email


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateEmailForm

# @login_required
# def update_email(request):
#     if request.method == 'POST':
#         form = UpdateEmailForm(request.POST)
#         if form.is_valid():
#             new_email = form.cleaned_data['email']
#             request.user.email = new_email
#             request.user.save()
#             messages.success(request, 'Your email has been updated successfully.')
#             return redirect(reverse('accounts:update_email'))
#     else:
#         form = UpdateEmailForm(initial={'email': request.user.email})
#     return render(request, 'accounts/update_email.html', {'form': form})

##vulnerable csrf

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import UpdateEmailForm

@login_required
def update_email(request):
    if request.method == 'POST':
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            # Ensure to handle cases where request.user is AnonymousUser
            if not request.user.is_anonymous:
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Your email has been updated successfully.')
            else:
                messages.error(request, 'You are not logged in.')
            return redirect(reverse('accounts:update_email'))
    else:
        form = UpdateEmailForm(initial={'email': request.user.email if not request.user.is_anonymous else ''})
    return render(request, 'accounts/update_email.html', {'form': form})



##end update email




# update/forgot password
def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def update_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            
            try:
                # user = User.objects.get(email=email, first_name=first_name, last_name=last_name)
                user = User.objects.get(email=email)
                new_password = generate_random_password()
                user.password = make_password(new_password)
                user.save()
                
                
                messages.success(request, f'Your new password is: {new_password}')
                
                return redirect('accounts:update_password')
            except User.DoesNotExist:
                messages.error(request, 'User with provided details does not exist.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'accounts/update_password.html', {'form': form})
    







##

# In views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import User

@user_passes_test(lambda u: u.is_superuser)
def delete_account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:  # Ensure the user being deleted is not an admin
        user.delete()
    return redirect('core:admin_users')


