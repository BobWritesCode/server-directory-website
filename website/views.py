
from .forms import (
    ProfileForm, CreateServerListingForm, ConfirmAccountDeleteForm,
    SignupForm, UserUpdateEmailAddressForm, ConfirmServerListingDeleteForm
)
from .models import CustomUser, ServerListing, Game, Tag, Bumps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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
import json

UserModel = get_user_model()


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
        # Let's see if the user is trying to delete the listing.
        if (
            ConfirmServerListingDeleteForm(request.POST, instance=request.user)
            and "server_listing_delete_confirm" in request.POST
        ):
            form_2 = ConfirmServerListingDeleteForm(request.POST)
            if (
                form_2.is_valid()
                and form_2.data["server_listing_delete_confirm"] == "delete"
            ):
                item.delete()
                return redirect("my-account")

        form = CreateServerListingForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if request.FILES:
                image = uploader.upload(request.FILES["logo"])
                form.instance.logo = image["url"]
            form.save()
            return redirect("my-account")

    form = CreateServerListingForm(instance=item)
    form_2 = ConfirmServerListingDeleteForm(instance=item)

    context = {
        "form": form,
        "form_2": form_2,
        "item": item,
    }
    return render(request, "server_edit.html", context)


@login_required
def server_delete(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)
    item.delete()
    return redirect('my-account')


@login_required
def my_account(request):
    if request.method == 'POST':
        # Check to see if the user is trying to update there email address.
        if (
            UserUpdateEmailAddressForm(request.POST, instance=request.user)
            and 'email_confirm' in request.POST
        ):
            form_3 = UserUpdateEmailAddressForm(request.POST)
            if form_3.is_valid():
                user = CustomUser.objects.get(email=request.user)
                # Flag email address as unverified
                user.email_verified = False
                # Save to database.
                user.save()
                # Send verification email to the user.
                send_email_verification(request, user, form_3)
                return redirect('signup_verify_email')

        # Let's see if the user is trying to delete a listing.
        if (
            ConfirmServerListingDeleteForm(request.POST, instance=request.user)
            and "server_listing_delete_confirm" in request.POST
        ):
            form_4 = ConfirmServerListingDeleteForm(request.POST)
            if (
                form_4.is_valid()
                and form_4.data["server_listing_delete_confirm"] == "delete"
            ):
                item_pk = form_4.data["itemID"]
                item = get_object_or_404(ServerListing, pk=item_pk)
                item.delete()
                return redirect("my-account")


        # Let's see if the user is trying to delete there account.
        if (
            ConfirmAccountDeleteForm(request.POST, instance=request.user)
            and 'account-delete-confirm' in request.POST
        ):
            form_2 = ConfirmAccountDeleteForm(request.POST)
            # Check if user has typed the correct phrase and hit submit
            if form_2.is_valid() and form_2.data['confirm'] == 'remove':
                CustomUser.objects.get(username=request.user).delete()
                return redirect(to='account_deleted')

    username = request.user
    queryset = ServerListing.objects.filter(
        owner=username).order_by('-created_on')
    num_of_listings = queryset.count()

    form = ProfileForm(instance=request.user)
    form_2 = ConfirmAccountDeleteForm(instance=request.user)
    form_3 = UserUpdateEmailAddressForm(instance=request.user)
    form_4 = ConfirmServerListingDeleteForm(instance=request.user)

    return render(
        request,
        'registration/my_account.html',
        {
            'form': form,
            'form_2': form_2,
            'form_3': form_3,
            'form_4': form_4,
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
            send_email_verification(request, user, form)
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
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()

        return redirect('email_address_verified')
    else:
        return HttpResponse('Activation link is invalid!')


def server_listings(request, slug, tag_string=""):
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()

    query = Q(status=1) & Q(game=game)
    queryset = ServerListing.objects.filter(query).distinct()

    # Get user bumps
    bumps_queryset = get_user_bumps(request)

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
            "server_listings": queryset,
            "bumps_queryset": bumps_queryset,
            "selected_tags": selected_tags,
            "tags": tags,
            "tag_string": tag_string,
            "slug": slug,
        },
    )


@login_required
def get_user_bumps(request):
    '''
    Returns a list of user's current bumps

        Parameters:
            request (Any): The server request

        Returns:
            bumps_queryset (list): List of user's active bumps
    '''
    query = Q(user=request.user)
    bumps_queryset = Bumps.objects.filter(query).values_list('listing_id')
    _list = [x[0] for x in bumps_queryset]
    return _list


class ServerDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = ServerListing.objects.filter(status=1)
        server = get_object_or_404(queryset, slug=slug)
        # Get user bumps
        bumps_queryset = get_user_bumps(request)

        return render(
            request,
            "server_detail.html",
            {
                "server": server,
                "bumps_queryset": bumps_queryset,
            },
        )


def send_email_verification(request, user, form):
    '''
    Send email address verification to user
    '''
    current_site = get_current_site(request)
    mail_subject = 'Verify your email address.'
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


def check_match(value1: str, value2: str):
    '''
    Returns bool depending if args match.
    :returns: True or False
    '''
    if value1 == value2:
        return True
    return False


def email_check(request):
    '''
    Check if email address already in use.
    '''
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['email']

    if CustomUser.objects.filter(email = content).exists():
        result = True
    else:
        result = False

    return HttpResponse ( json.dumps({'result': result}) )


@login_required
def bump_server(request):
    '''
    Add 1 bump to server if already not bumped by user
    '''
    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['server_id']

        # Get server listing object
        listing = get_object_or_404(ServerListing, id=content)

        # Get user bumps
        bumps_queryset = get_user_bumps(request)
        bumps_queryset_len = len(bumps_queryset) + 1
        print(bumps_queryset_len)

        # Check if this server already bumped by user
        if (content in bumps_queryset):
            return HttpResponse ( json.dumps({'result': int(bumps_queryset_len)}) )

        # Check user has not already bumped max server amount
        if len(bumps_queryset) > 4:
            return HttpResponse ( json.dumps({'result': int(bumps_queryset_len)}) )

        # Create a row to table and save
        bump = Bumps.objects.create(user=request.user, listing=listing )
        bump.save()
        return HttpResponse ( json.dumps({'result': int(bumps_queryset_len)}) )