from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
 
from . import views

from .views import DepositMoneyView, PaymentView, TransferView, WithdrawMoneyView, TransactionRepostView, profile


app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path('profile/', views.profile, name='profile'),
    path('transact/', views.transact, name='transact'),
    path('transfer/', TransferView.as_view(), name='transfer_form'),
    path('payment/', PaymentView.as_view(), name='payment_form'),
    path('apply-fd/', views.apply_fd, name='apply_fd'),
    path('apply-rd/', views.apply_rd, name='apply_rd'),
    path('application-success/', views.application_success, name='application_success'),
    path('fd-applications/', views.user_fd_applications, name='user_fd_applications'),
    path('rd-applications/', views.user_rd_applications, name='user_rd_applications'),
    path('fd-rd/', views.fd_rd, name='fd_rd'),
    path('approve-fd/<int:application_id>/', views.approve_fd_application, name='approve_fd_application'),
    path('reject-fd/<int:application_id>/', views.reject_fd_application, name='reject_fd_application'),
    path('approve-rd/<int:application_id>/', views.approve_rd_application, name='approve_rd_application'),
    path('reject-rd/<int:application_id>/', views.reject_rd_application, name='reject_rd_application'),
    path('status/', views.check_status, name='check_status'),
    path('fd-application/delete/<int:application_id>/', views.delete_fd_application, name='delete_fd_application'),
    path('rd-application/delete/<int:application_id>/', views.delete_rd_application, name='delete_rd_application'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

