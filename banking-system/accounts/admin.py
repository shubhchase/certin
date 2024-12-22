from distro import like
from django.contrib import admin

from .models import BankAccountType, User, UserAddress, UserBankAccount


admin.site.register(BankAccountType)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)
# admin.site.register(Profile)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['action_checkbox', 'Profile']

    def get_list_display(self, request):
        return ['action_checkbox'] + super().get_list_display(request)
    
    
    
    ###


class UserBankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_no', 'account_type', 'gender', 'birth_date')
    list_filter = ('user', 'account_no', 'account_type', 'gender', 'birth_date')  # Add filters based on your needs
###