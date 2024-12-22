from django.conf import settings
from django.urls import path
from . import views

from django.conf.urls.static import static


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.comment_post, name='comment_post'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('blogs/', views.blogs, name='blogs'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact_view, name='contact'),
    path('error/', views.error, name='error'),
    path('adminpanel/', views.adminpanel, name='adminpanel'),
    path('admin_transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('contact-messages/', views.admin_contact, name='admin_contact'),
    path('contact-messages/<int:message_id>/delete/', views.delete_contact, name='delete_contact'),
    path('blog-posts/', views.admin_blog_posts, name='admin_blog_posts'),
    path('blog-posts/add/', views.add_blog_post, name='add_blog_post'),
    path('blog-posts/<int:post_id>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('blog-posts/<int:post_id>/delete/', views.delete_blog_post, name='delete_blog_post'),
    path('request/', views.fd_rd_request, name='fd_rd_request'),
    path('star-user/', views.star_user, name='star_user'),
    path('notification/', views.user_notifications, name='user_notifications'),
    path('service-request/', views.create_service_request, name='service_request'),
    path('service-request-success/', views.service_request_success, name='service_request_success'),
    path('service-requests/', views.admin_service_requests, name='admin_service_requests'),
    path('service-requests/<int:pk>/<str:status>/', views.change_request_status, name='change_request_status'),
    path('service-requests-status/', views.service_requests_status, name='service_requests_status'),
    path('service-requests/delete/<int:pk>/', views.delete_service_request, name='delete_service_request'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
