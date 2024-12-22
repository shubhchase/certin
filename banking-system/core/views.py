from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Like, ContactMessage
from .forms import BlogPostForm, CommentForm, ContactForm
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from transactions.constants import DEPOSIT, TRANSFER, WITHDRAWAL, PAYMENT



class HomeView(TemplateView):
    template_name = 'core/index.html'


def index(request):
    # blog_posts = BlogPost.objects.all()
    # context = {
    #     'blog_posts': blog_posts,
    # }
    return render(request, 'core/index.html')

@login_required
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
    
    # Determine the redirect URL based on referer or another logic
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('core:blogs')  # Default fallback redirect

@login_required
def unlike_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    like = Like.objects.filter(post=post, user=request.user).first()
    
    if like:
        like.delete()
    
    # Determine the redirect URL based on referer or another logic
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('core:blogs')  # Default fallback redirect

@login_required
def comment_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('core:post_detail', pk=pk)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comment_form': form,
    }
    return render(request, 'core/post_detail.html', context)



def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comment_form = CommentForm()

    if pk == 1:
        template_name = 'core/blog_post_1.html'
    elif pk == 2:
        template_name = 'core/blog_post_2.html'
    elif pk == 3:
        template_name = 'core/blog_post_3.html'
    else:
        template_name = 'core/post_detail.html'

    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, template_name, context)


def about(request):
    return render(request, 'core/about.html')
def services(request):
    return render(request, 'core/services.html')
def projects(request):
    return render(request, 'core/projects.html')
def team(request):
    return render(request, 'core/team.html')
def testimonial(request):
    return render(request, 'core/testimonial.html')
def faq(request):
    return render(request, 'core/faq.html')
def error(request):
    return render(request, 'core/error.html')
def messagess(request):
    return render(request, 'core/messages.html')
# def adminpanel(request):
#     return render(request, 'core/adminpanel.html')
def blogs(request):
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'core/blogs.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


from accounts.models import UserBankAccount
from transactions.models import FDApplication, Notification, RDApplication, Transaction
from .decorators import admin_required


@login_required
@admin_required
def adminpanel(request):
    # Get the total count of UserBankAccount instances
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    
    
    # Render the template with the counts
    return render(request, 'core/adminpanel.html', {
        'account_count': account_count,
        'transaction_count': transaction_count,
        
    })
    
@login_required
@admin_required
def admin_transactions(request):
    # Get the total count of UserBankAccount instances
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    transactions = Transaction.objects.all()
    
    # Render the template with the counts
    return render(request, 'core/admin_transactions.html', {
        'account_count': account_count,
        'transaction_count': transaction_count,
        'transactions': transactions,
    })

from accounts.models import UserBankAccount
from accounts.models import UserAddress

@login_required
@admin_required
def admin_users(request):
        # Get the total count of UserBankAccount instances
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    users = UserBankAccount.objects.select_related('user__address').all()
    
    return render(request, 'core/admin_users.html', {
        'account_count': account_count,
        'transaction_count': transaction_count,
        'users': users,
        
        
    })
    
    
    ##admin panel contact us details
    

@login_required
@admin_required
def admin_contact(request):
    contact_messages = ContactMessage.objects.all()
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    return render(request, 'core/admin_contact.html', {'contact_messages': contact_messages,'account_count': account_count,
        'transaction_count': transaction_count,})

@login_required
@admin_required
@require_POST    
def delete_contact(request, message_id):
    contact_message = get_object_or_404(ContactMessage, id=message_id)
    contact_message.delete()
    return redirect('core:admin_contact')   

@login_required
@admin_required
def admin_blog_posts(request):
    blog_posts = BlogPost.objects.all()
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    return render(request, 'core/admin_blog_posts.html', {'blog_posts': blog_posts,'account_count': account_count,
        'transaction_count': transaction_count,})

@login_required
@admin_required
def add_blog_post(request):
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    if request.method == 'POST':
        # Handle form submission
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:admin_blog_posts')
    else:
        form = BlogPostForm()
    return render(request, 'core/add_blog_post.html', {'form': form,'account_count': account_count,
        'transaction_count': transaction_count,})

@login_required
@admin_required
def edit_blog_post(request, post_id):
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('core:admin_blog_posts')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'core/edit_blog_post.html', {'form': form,'account_count': account_count,
        'transaction_count': transaction_count,})

@require_POST
@login_required
@admin_required
def delete_blog_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    blog_post.delete()
    return redirect('core:admin_blog_posts')


##FD and RD

@login_required
@admin_required
def fd_rd_request(request):
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    fd_applications = FDApplication.objects.all()
    rd_applications = RDApplication.objects.all()
    return render(request, 'core/admin_custom.html', {
        'fd_applications': fd_applications,
        'rd_applications': rd_applications,
        'account_count': account_count,
        'transaction_count': transaction_count,

    })

# views.py

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from accounts.models import UserBankAccount
from transactions.models import Transaction  # Make sure to import the Transaction model
from transactions.models import Notification  # Import Notification model
from .forms import StarUserForm
from transactions.constants import TRANSFER

@user_passes_test(lambda u: u.is_superuser)
def star_user(request):
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    if request.method == 'POST':
        form = StarUserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            amount = form.cleaned_data['amount']
            user_account = get_object_or_404(UserBankAccount, user_id=user_id)

            # Calculate new balance
            new_balance = user_account.balance + amount

            # Create a transaction record
            Transaction.objects.create(
                account=user_account,
                transaction_type=TRANSFER,
                amount=amount,
                balance_after_transaction=new_balance,
                description='Star User Award'
            )

            # Update the user's balance
            user_account.balance = new_balance
            user_account.save()

            # Save a notification for the user
            Notification.objects.create(
                user=user_account.user,
                message=f'Congratulations! You have been selected as a star user and awarded {amount}.'
            )

            messages.success(request, 'Star user selected and amount added successfully.')
            return redirect('core:star_user')
    else:
        form = StarUserForm()

    return render(request, 'core/star_user.html', {'form': form,'account_count': account_count,
        'transaction_count': transaction_count,})


from transactions.models import Notification
@login_required
def user_notifications(request):
    notifications = request.user.notifications.all()
    return render(request, 'core/notification.html', {'notifications': notifications})

 

from .forms import ServiceRequestForm

@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            return redirect('core:service_request_success')
    else:
        form = ServiceRequestForm()
    return render(request, 'core/service_request.html', {'form': form})

def service_request_success(request):
    return render(request, 'core/service_request_success.html')    


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import ServiceRequest

@staff_member_required
def admin_service_requests(request):
    service_requests = ServiceRequest.objects.all()
    account_count = UserBankAccount.objects.count() 
    # Get the total count of Transaction instances
    transaction_count = Transaction.objects.count()
    return render(request, 'core/service_requests.html', {'service_requests': service_requests,'account_count': account_count,
        'transaction_count': transaction_count,})

@staff_member_required
def change_request_status(request, pk, status):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    service_request.status = status
    service_request.save()
    return redirect('core:admin_service_requests')

@login_required
def service_requests_status(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'core/service_requests_status.html', {'service_requests': service_requests})

@staff_member_required
def delete_service_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    service_request.delete()
    messages.success(request, "Service request deleted successfully.")
    return redirect('core:admin_service_requests')




