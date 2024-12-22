from django.contrib import admin
from .models import FDApplication, Notification, RDApplication
from django.core.mail import send_mail
from transactions.models import Transaction

admin.site.register(Transaction)
# admin.site.register(Payment)
# admin.site.register(Transfer)


class FDApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'tenure', 'interest_rate', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'amount')
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        rows_updated = queryset.update(status='Approved')
        self.message_user(request, f"{rows_updated} FD applications were approved.")
    approve_selected.short_description = "Approve selected FD applications"

    def reject_selected(self, request, queryset):
        rows_updated = queryset.update(status='Rejected')
        self.message_user(request, f"{rows_updated} FD applications were rejected.")
    reject_selected.short_description = "Reject selected FD applications"

class RDApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'monthly_amount', 'tenure', 'interest_rate', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'amount')
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        rows_updated = queryset.update(status='Approved')
        self.message_user(request, f"{rows_updated} RD applications were approved.")
    approve_selected.short_description = "Approve selected RD applications"

    def reject_selected(self, request, queryset):
        rows_updated = queryset.update(status='Rejected')
        self.message_user(request, f"{rows_updated} RD applications were rejected.")
    reject_selected.short_description = "Reject selected RD applications"

# admin.py
from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at',)

admin.site.register(Notification, NotificationAdmin)


admin.site.register(FDApplication, FDApplicationAdmin)
admin.site.register(RDApplication, RDApplicationAdmin)
