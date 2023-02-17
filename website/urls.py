"""
All urls for app.
"""

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import (
    PasswordChangeForm, SetPasswordForm, PasswordResetForm
)
from django.urls import path

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
        views.listing_detail,
        name='listing_detail'
    ),

    path(
        'accounts/my_account',
        views.my_account,
        name='my-account'
    ),

    path(
        'accounts/login',
        views.login_view,
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

    path(
        'activate/<uidb64>/<token>/',
        views.activate,
        name='activate'
    ),

    path(
        'accounts/password_reset',
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            form_class=PasswordResetForm,
            subject_template_name='email_templates/password_reset_subject.txt',
            email_template_name='email_templates/password_reset_email.html',
            success_url='password_reset_done',
        ),
        name='password_reset'
    ),

    path(
        'accounts/password_reset_done',
        auth_views.PasswordResetDoneView.as_view(
        ),
        name='password_reset_done'
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
        'server_edit/<_pk>',
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

    path(
        'game_management',
        views.game_management,
        name='game_management'
    ),

    path(
        'tag_management',
        views.tag_management,
        name='tag_management'
    ),

    path(
        'staff_user_management_search',
        views.staff_user_management_search,
        name='staff_user_management_search'
    ),

    path(
        'staff_user_management_user/<_id>',
        views.staff_user_management_user,
        name='staff_user_management_user'
    ),

    path(
        'terms_and_conditions',
        views.terms_and_conditions,
        name='terms_and_conditions'
    ),

    path(
        'privacy_policy',
        views.privacy_policy,
        name='privacy_policy'
    ),

    path(
        'contact_us',
        views.contact_us,
        name='contact_us'
    ),

    path(
        'unauthorized',
        views.unauthorized,
        name='unauthorized'
    ),

    path(
        '404',
        views.e404,
        name='404'
    ),

]
