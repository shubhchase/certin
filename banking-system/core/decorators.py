from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser,
        login_url='/transactions/profile/'  # Redirect to login page if the user is not an admin
    )(view_func)
    return decorated_view_func
