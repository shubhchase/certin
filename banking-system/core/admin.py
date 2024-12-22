from django.contrib import admin
from .models import Like, Comment, BlogPost, ContactMessage, ServiceRequest


admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(BlogPost)
admin.site.register(ContactMessage)
# Register your models here.

# class BlogPostAdmin(admin.ModelAdmin):
#     list_display=('id','title','content','image','author','date_posted')

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service_type', 'status', 'created_at')
    list_filter = ('status', 'service_type')
    search_fields = ('name', 'email', 'purpose')
    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        queryset.update(status='accepted')

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')

    accept_requests.short_description = "Accept selected requests"
    reject_requests.short_description = "Reject selected requests"

admin.site.register(ServiceRequest, ServiceRequestAdmin)