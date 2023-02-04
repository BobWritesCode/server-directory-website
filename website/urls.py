from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm,
    SetPasswordForm
)
from django.urls import path, reverse_lazy


from . import views

urlpatterns = [
    path(
        '',
        views.index,
        name='home'
    ),

    path(
        'server-list/<str:slug>',
        views.server_listings,
        name='server-list'
    ),

    path(
        'server-list/<str:slug>/<str:tag_string>',
        views.server_listings,
        name='server-list-wth-tags'
    ),

    path(
        'server/<slug>',
        views.server_detail,
        name='server_detail'
    ),

    path(
        'accounts/my_account',
        views.my_account,
        name='my-account'
    ),

    path(
        'accounts/login',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=AuthenticationForm,
            success_url=reverse_lazy("home"),
        ),
        name='login'
    ),

    path(
        'accounts/signup',
        views.sign_up_view,
        name='signup'
    ),

    path(
        'accounts/signup_verify_email',
        views.signup_verify_email,
        name='signup_verify_email'
    ),

    path('activate/<uidb64>/<token>/',
    views.activate,
    name='activate'
    ),

    path(
        'accounts/email_address_verified',
        views.email_address_verified,
        name='email_address_verified'
        ),

    path(
        'accounts/password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url='password_change_done',
            form_class=PasswordChangeForm,
            extra_context={},
        ),
        name='password_change'
    ),

    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            success_url='password_reset_done',
            form_class=PasswordResetForm,
            extra_context={},
        ),
        name='password_reset'
    ),

    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url='password_reset_complete',
            form_class=SetPasswordForm,
            extra_context={},
        ),
        name='password_reset_confirm'
    ),

    path(
        'accounts/account_deleted/',
        views.account_deleted,
        name='account_deleted'
    ),

    path(
        'server_create',
        views.server_create,
        name='server_create'
    ),

    path(
        'server_edit/<item_pk>',
        views.server_edit,
        name='server_edit'
    ),

    path(
        'server_delete/<item_pk>',
        views.server_delete,
        name='server_delete'
    ),

    path(
        'request',
        views.email_check,
        name='email_check'
    ),

    path(
        'bump_server',
        views.bump_server,
        name='bump_server'
    ),

    path(
        'staff_account',
        views.staff_account,
        name='staff_account'
    ),

    path(
        'staff_image_review',
        views.staff_image_review,
        name='staff_image_review'
    ),

    path(
        'staff_image_review/<item_pk>',
        views.staff_image_review,
        name='staff_image_review_with_id'
    ),

    path(
        'call_server',
        views.call_server,
        name='call_server'
    ),
]
