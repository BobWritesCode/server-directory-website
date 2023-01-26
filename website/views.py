
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy
from django.views import View, generic
from cloudinary import uploader

UserModel = get_user_model()

from .models import ServerListing, Game, Tag
from .forms import (
    ProfileForm, CreateServerListingForm, ConfirmAccountDeleteForm,
    SignupForm
)


def send_mail_tu_user():
    send_mail(
        'Subject here',
        'Here is the message.',
        'contact@warwickhart.com',
        ['warwick_hart@hotmail.com'],
        fail_silently=False,
    )


def index(request):
    games = Game.objects.filter(status=1)
    ctx = {
        'games': games,
        'tag_string': "0",
    }
    return render(request, "index.html", ctx)


def account_deleted(request):
    return render(request, "registration/account_deleted.html")


def signup_verify_email(request):
    return render(request, "registration/signup_verify_email.html")

def email_address_verified(request):
    return render(request, "registration/email_address_verified.html")
    email_address_verified


@login_required
def server_create(request):
    if request.method == 'POST':
        form = CreateServerListingForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                image = uploader.upload(request.FILES['logo'])
                form.instance.logo = image['url']
            form.instance.owner = request.user
            form.save()
            return redirect('my-account')
        else:
            return render(
                request,
                "server_create.html",
                {
                    'form': form,
                }
            )

    return render(
        request,
        "server_create.html",
        {
            'form': CreateServerListingForm(),
        }
    )


@login_required
def server_edit(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)
    if request.method == "POST":
        form = CreateServerListingForm(
            request.POST, request.FILES, instance=item)
        if form.is_valid():
            if request.FILES:
                image = uploader.upload(request.FILES['logo'])
                form.instance.logo = image['url']
            form.save()
            return redirect('my-account')

    form = CreateServerListingForm(instance=item)

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'server_edit.html', context)


@login_required
def server_delete(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)
    item.delete()
    return redirect('my-account')


@login_required
def my_account(request):
    if request.method == 'POST':
        # Let's see if the user is trying to delete there account.
        if (
            ConfirmAccountDeleteForm(request.POST, instance=request.user)
            and 'account-delete-confirm' in request.POST
        ):
            form_2 = ConfirmAccountDeleteForm(request.POST)
            # Check if user has typed the correct phrase and hit submit
            if form_2.is_valid() and form_2.data['confirm'] == 'remove':
                User.objects.get(username=request.user).delete()
                return redirect(to='account_deleted')

        # Check to see if user is trying to update their email address.
        # If so, then save new email address to database.
        if (
            ProfileForm(request.POST, instance=request.user)
            and 'account-email-update' in request.POST
        ):
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Your profile is updated successfully')
                # return redirect(to='my-account')

    username = request.user
    queryset = ServerListing.objects.filter(
        owner=username).order_by('-created_on')
    num_of_listings = queryset.count()
    form = ProfileForm(instance=request.user)
    form_2 = ConfirmAccountDeleteForm(instance=request.user)

    return render(
        request,
        'registration/my_account.html',
        {
            'form': form,
            'form_2': form_2,
            "server_listing": queryset,
            'num_of_listings': num_of_listings,
        }
    )


def sign_up_view(request):
    """
    User create account view
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # Check user has completed form as required.
        if form.is_valid():
            # Original code before modifications, check ReadMe:
            # https://shafikshaon.medium.com/
            # user-registration-with-email-verification-in-django-8aeff5ce498d
            # Saving user to memory as inactive.
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Prepare email to be sent.
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_templates/verify_email_address.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # Send email to user.
            send_mail(
                subject=mail_subject,
                message=message,
                from_email='contact@warwickhart.com',
                recipient_list=[to_email]
            )
            # Direct user to next page.
            return redirect('signup_verify_email')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    '''
    Activate user account after they have they visited the link in the
    email address verification, sent to the user by email.
    '''
    # Original code:
    # https://shafikshaon.medium.com/
    # user-registration-with-email-verification-in-django-8aeff5ce498d
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email_address_verified')
    else:
        return HttpResponse('Activation link is invalid!')


def server_listings(request, slug, tag_string=""):
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()

    query = Q(status=1) & Q(game=game)
    queryset = ServerListing.objects.filter(query).distinct()

    all_tags_for_game = []
    for x in tags:
        all_tags_for_game.append([x.id, x.name])

    ' Manage tag_string'
    if tag_string != "":
        'Create list from string'
        selected_tags = tag_string.split("%")
        'Check to see if adding or removing tag'
        action = selected_tags.pop(0)

        'A = add tag, R = remove tag'
        if action == "A":
            'Prepare new tag_string to send to front-end'
            tag_string = '%' + '%'.join(selected_tags)

        else:
            'Which tag has been selected to be removed'
            to_be_removed = selected_tags.pop(0)

            'Remove tag from selected list'
            selected_tags.remove(to_be_removed)

            'Check to see if all tags have been unselected'
            'Prepare tag_string'
            if len(selected_tags) != 0:
                tag_string = '%' + '%'.join(selected_tags)
            else:
                tag_string = ''

        'Narrows server list down based on tags picked by user'
        for value in selected_tags:
            queryset = queryset.filter(tags__name=value)

        'Use list comprehension to remove selected tags from all available tags'
        tags = [x for x in game.tags.all() if x.name not in selected_tags]

    else:
        'If tag_string empty then create empty list'
        selected_tags = []
        'Get all available tags for game selected'
        tags = game.tags.all()

    return render(
        request,
        "server-list.html",
        {
            "serverlisting": queryset,
            "selected_tags": selected_tags,
            "tags": tags,
            "tag_string": tag_string,
            "slug": slug,
        },
    )


class ServerDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = ServerListing.objects.filter(status=1)
        server = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "server_detail.html",
            {
                "server": server,
            },
        )
