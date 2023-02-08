from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy
from django.views import View, generic

from cloudinary import uploader
from datetime import timedelta, date
import json
import re


from .constants import DAYS_TO_EXPIRE_IMAGE

from .forms import (
    ProfileForm, CreateServerListingForm, ConfirmAccountDeleteForm,
    SignupForm, UserUpdateEmailAddressForm, ConfirmServerListingDeleteForm,
    ImageForm, LoginForm, GameManageForm, ConfirmGameDeleteForm,
    ConfirmTagDeleteForm, TagsManageForm, UserForm, DeleteConfirmForm
)
from .models import (
    CustomUser, ServerListing, Game, Tag, Bumps, Images
)


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


def terms_and_conditions(request):
    return render(request, "terms_and_conditions.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def contact_us(request):
    return render(request, "contact_us.html")


@login_required
@staff_member_required
def staff_account(request):
    query = Q(status=0)
    review_count = Images.objects.filter(query)

    return render(
        request,
        "staff/staff_account.html",
        {
            'img_need_review_count': len(review_count),
        },
    )


@login_required
@staff_member_required
def staff_image_review(request, item_pk: int = None):
    # If ID has been entered in URL.
    if item_pk:
        query = Q(pk=item_pk)
        image = Images.objects.filter(query).first()
        # If ID for image does not exist, handle request.
        if not image:
            return redirect('staff_account')
    # If no ID has been entered in URL.
    else:
        query = Q(status=0)
        image = Images.objects.filter(query).first()
        # If no image is currently waiting be approved, then handle request.
        if image is None:
            return redirect('staff_account')
            # # Show image first in Q.
            # return redirect('staff_image_review_with_id', image.pk)

    # Set status text based on image.status.
    match image.status:
        case 0:
            image.status_txt = "Awaiting approval"
        case 1:
            image.status_txt = "Image approved"
        case 2:
            image.status_txt = "Image declined, User banned"

    return render(
        request,
        "staff/staff_image_review.html",
        {
            'image': image,
        },
    )


@login_required
def server_create(request):

    if request.method == 'POST':

        form = CreateServerListingForm(request.POST)
        image_form = ImageForm(request.FILES)

        if form.is_valid() and image_form.is_valid():

            form.instance.owner = request.user
            form.save()

            if request.FILES:
                new_image = uploader.upload(request.FILES['image'])
                image_form.instance.image = new_image['url']
                image_form.instance.public_id = new_image['public_id']
                image_form.instance.user = request.user
                image_form.instance.listing = get_object_or_404(
                    ServerListing, pk=form.instance.id)
                image_form.instance.approved_by = None
                image_form.save()

            return redirect('my-account')

        else:
            return render(
                request,
                "server_create.html",
                {
                    'form': form,
                    'image_form': image_form,
                }
            )

    return render(
        request,
        "server_create.html",
        {
            'form': CreateServerListingForm(),
            'image_form': ImageForm(),
            'tags': Tag.objects.all(),
        }
    )


@login_required
def server_edit(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)

    query = Q(serverlisting=item)
    selected_tags = Tag.objects.filter(query)

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

        # If user is trying to update the listing
        form = CreateServerListingForm(request.POST, instance=item)
        image_form = ImageForm(request.FILES)

        if form.is_valid() and image_form.is_valid():

            if request.FILES:

                image = Images.objects.filter(listing_id = item_pk).first()

                if image is not None:
                    # Delete old image from Cloudinary server
                    uploader.destroy(image.public_id)
                    # Upload new imaged
                    new_image = uploader.upload(request.FILES['image'])
                else:
                    # Upload new imaged
                    new_image = uploader.upload(request.FILES['image'])
                    image = image_form.instance
                    image.user = request.user
                    image.listing = get_object_or_404(ServerListing, pk=form.instance.id)

                image.date_added = date.today()
                image.status = 0
                image.reviewed_by = None
                image.image = new_image['url']
                image.public_id = new_image['public_id']
                image.approved_by = None
                image.save()


            form.save()

            return redirect("my-account")

    # Set status text based on image.status.
    try:
        # Get images for server listings
        # Makes sure they are status 1: approved.
        query =  Q(listing_id=item.id)
        listing_image = Images.objects.filter(query).first()

        match listing_image.status:
            case 0:
                listing_image.status_txt = "Awaiting approval"
            case 1:
                listing_image.status_txt = "Image approved"
            case 2:
                listing_image.status_txt = "Image declined, User banned"
    except AttributeError:
        listing_image = None

    context = {
        "form": CreateServerListingForm(instance=item),
        "form_2": ConfirmServerListingDeleteForm(instance=item),
        "item": item,
        'image_form': ImageForm(),
        'listing_image': listing_image,
        'tags': Tag.objects.all(),
        'selected_tags': serializers.serialize('json', selected_tags),
    }
    return render(request, "server_edit.html", context)


@login_required
def server_delete(request, item_pk):
    item = get_object_or_404(ServerListing, pk=item_pk)

    image = Images.objects.filter(listing_id = item_pk).first()
    if image is not None:
        # Delete listing image from Cloudinary server
        uploader.destroy(image.public_id)

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

                # Get current image for listing
                item = get_object_or_404(ServerListing, pk=item_pk)
                image = Images.objects.filter(listing_id=item_pk).first()
                if image is not None:
                    # Delete listing image from Cloudinary server
                    uploader.destroy(image.public_id)

                # Delete server listing from database
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
    server_listings = ServerListing.objects.filter(
        owner=username).order_by('-created_on')
    num_of_listings = server_listings.count()

    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in server_listings.values_list('id')]
    query = Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()

    # Pair images with server listing
    for index, value in enumerate(server_listings):
        # try to pair image with server listing, if image not available or does not
        # exist then set as None so a placeholder can be shown instead.
        try:
            image = images_queryset.get(listing_id = server_listings[index].id).image

            match images_queryset.get(listing_id = server_listings[index].id).status:
                case 0:
                    status = "Awaiting review"
                case 1:
                    status = "Approved"
                case 2:
                    status = "Rejected"
                case 3:
                    status = "Banned"

        except ObjectDoesNotExist:
            image = None
            status = None
        finally:
            server_listings[index].image_url = image
            server_listings[index].image_status = status

    form = ProfileForm(instance=request.user)
    form_2 = ConfirmAccountDeleteForm(instance=request.user)
    form_3 = UserUpdateEmailAddressForm(instance=request.user)
    form_4 = ConfirmServerListingDeleteForm(instance=request.user)

    # Get user bumped servers
    query = Q(user=request.user)
    bumps_queryset = Bumps.objects.filter(query)
    # Get server queryset based on users bumped servers
    query = Q(pk__in=bumps_queryset.values_list('listing_id'))
    server_listings_queryset = ServerListing.objects.filter(query)
    # Add server listing slug to bumps queryset
    for index, value in enumerate(bumps_queryset):
        bumps_queryset[index].url = server_listings_queryset.get(
            id=value.listing.id).slug
    # Calculate how many bumps the user has left to use
    bumps_left = 5 - len(bumps_queryset)

    return render(
        request,
        'registration/my_account.html',
        {
            'form': form,
            'form_2': form_2,
            'form_3': form_3,
            'form_4': form_4,
            'server_listings': server_listings,
            'num_of_listings': num_of_listings,
            'bumps': bumps_queryset,
            'bumps_left': bumps_left,
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
    listings_queryset = ServerListing.objects.filter(query).distinct()

    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in listings_queryset.values_list('id')]
    query = Q(status=1) & Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()

    # Get user bumps
    bumps_queryset = get_user_bumps(request)

    all_tags_for_game = []
    for x in tags:
        all_tags_for_game.append([x.id, x.name])

    # Manage tag_string
    if tag_string != "":
        # Create list from string
        selected_tags = tag_string.split("%")
        # Check to see if adding or removing tag
        action = selected_tags.pop(0)

        # A = add tag, R = remove tag
        if action == "A":
            # Prepare new tag_string to send to front-end
            tag_string = '%' + '%'.join(selected_tags)

        else:
            # Which tag has been selected to be removed
            to_be_removed = selected_tags.pop(0)

            # Remove tag from selected list
            selected_tags.remove(to_be_removed)

            # Check to see if all tags have been unselected
            # Prepare tag_string
            if len(selected_tags) != 0:
                tag_string = '%' + '%'.join(selected_tags)
            else:
                tag_string = ''

        # Narrows server list down based on tags picked by user
        for value in selected_tags:
            listings_queryset = listings_queryset.filter(tags__name=value)

        # Use list comprehension to remove selected tags from all available tags
        tags = [x for x in game.tags.all() if x.name not in selected_tags]

    else:
        # If tag_string empty then create empty list
        selected_tags = []
        # Get all available tags for game selected
        tags = game.tags.all()

    # Pair images with server listing
    for index, value in enumerate(listings_queryset):
        # try to paid image with server listing, if image not available or does not
        # exist then set as None so a placeholder can be shown instead.
        try:
            image = images_queryset.get(listing_id=listings_queryset[index].id).image
        except ObjectDoesNotExist:
            image = None
        finally:
            listings_queryset[index].image_url = image

    return render(
        request,
        "server-list.html",
        {
            "server_listings": listings_queryset,
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


def server_detail(request, slug):

    # Get correct listing, check if approved.
    queryset = ServerListing.objects.filter(status=1)
    server = get_object_or_404(queryset, slug=slug)

    # Get user bumps.
    bumps_queryset = get_user_bumps(request)

    # Get listing approved images.
    query = Q(status=1) & Q(listing_id=server.id)
    images = Images.objects.filter(query).distinct()

    return render(
        request,
        "server_detail.html",
        {
            "images": images,
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


@staff_member_required
@login_required
def call_server(request):
    '''
    Generic method for front end to call backend with a request.
    '''

    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['arguments']

        match content['0']:
            case 'image_approval_approve':
                item = get_object_or_404(Images, pk=content['1'])
                item.status = 1
                item.expiry = None
                item.reviewed_by = request.user
                item.save()
                result = {
                    'success': True,
                    'text': "Approved"
                }

            case 'image_approval_reject':
                item = get_object_or_404(Images, pk=content['1'])
                item.status = 2
                item.expiry = date.today() + timedelta(days=DAYS_TO_EXPIRE_IMAGE)
                item.reviewed_by = request.user
                item.save()
                result = {
                    'success': True,
                    'text': "Rejected"
                }

            case 'image_approval_ban':
                item = get_object_or_404(Images, pk=content['1'])
                item.status = 3
                item.expiry = date.today() + timedelta(days=DAYS_TO_EXPIRE_IMAGE)
                item.reviewed_by = request.user
                item.save()
                ban_user(item.user_id)
                result = {
                    'success': True,
                    'text': "Rejected and user banned"
                }

            case 'image_approval_next':
                query = Q(status=0)
                image = Images.objects.filter(query).first()
                # If no image is currently waiting be approved, then handle request.
                if image is None:
                    result = {
                        'success': True,
                        'text': "/staff_account",
                    }
                else:
                    result = {
                        'success': True,
                        'text': f"/staff_image_review/{image.pk}",
                    }

            case 'get_game_details':
                game = get_object_or_404(Game, pk=content['1'])
                query = Q(game=content['1'])
                tags = Tag.objects.filter(query)
                result = {
                    'success': True,
                    'game': game.toJSON(),
                    'game_tags':serializers.serialize('json', tags),
                }

            case 'get_tag_details':
                tag = get_object_or_404(Tag, pk=content['1'])
                result = {
                    'success': True,
                    'tag': tag.toJSON(),
                }

            case 'search_users-username':
                query = Q(username__contains=content['1'])
                users = CustomUser.objects.filter(query)
                result = {
                    'success': True,
                    'users': serializers.serialize('json', users),
                }

            case 'search_users-email':
                query = Q(email__contains=content['1'])
                users = CustomUser.objects.filter(query)
                result = {
                    'success': True,
                    'users': serializers.serialize('json', users),
                }

            case 'search_users-id':
                query = Q(id__contains=int(content['1']))
                users = CustomUser.objects.filter(query)
                result = {
                    'success': True,
                    'users': serializers.serialize('json', users),
                }

            case 'user_management_save':
                success = update_user(content['1'])
                result = {
                    'success': success['result'],
                    'reason': success['reason']
                }

        return HttpResponse(json.dumps({'result': result}))

@staff_member_required
@login_required
def ban_user(user_id):
    '''
    Prevents user login, rejects all images for deletion, unpublish listings.
    '''
    # Set user to is banned.
    user = get_object_or_404(CustomUser, pk=user_id)

    # Delete all current user sessions (in case logged in on multiple devices)
    [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]

    user.is_banned = True
    user.save()

    # Unpublish all listings
    query = Q(owner_id = user_id)
    ServerListing.objects.filter(query).update(status=0)

    # Unpublish all images and set for deletion
    query = Q(user_id = user_id)
    image_expire = date.today() + timedelta(days = DAYS_TO_EXPIRE_IMAGE)
    Images.objects.filter(query).update(status = 3, expiry = image_expire)


def login_view(request):

    error_message = None

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user.is_banned:
            error_message = "This account is banned."
            user = None
        elif user is not None:
            login(request, user)
            return redirect("my-account")
        else:
            error_message = "Either user does not exist or password does not match account."

    form = LoginForm()

    return render(
        request,
        "registration/login.html",
        {
            "form": form,
            "error_message": error_message,
        },
    )


@staff_member_required
@login_required
def game_management(request: object):
    """
    request.GET: Loads html page using render().

    request.POST: Processes adding, updating and deleting games.

    Args:
        request (object): request data received from POST

    Returns:
        render: Loads html page
    """

    if request.method == "POST":

        # New listing flag - default to False
        new_listing = False

        # Let's see if the user is trying to delete a game.
        if (
            ConfirmGameDeleteForm(request.POST)
            and "game_delete_confirm" in request.POST
        ):
            form = ConfirmGameDeleteForm(request.POST)
            delete_game(form)
            return redirect("game_management")

        # Checking if updating a current game
        elif request.POST["id"]:
            form = GameManageForm(
                request.POST, instance=get_object_or_404(Game, pk=request.POST["id"])
            )
            # New listing flag - False
            new_listing = False

        # Or if inputting a new game
        else:
            form = GameManageForm(request.POST)
            # New listing flag - True
            new_listing = True
            # Allow object to the edited
            request.POST._mutable = True
            # Get next ID and assign slug
            form.data["id"] = Game.objects.order_by("-id").first().id + 1
            form.data["slug"] = form.data["slug"]
            # Restrict object from being edited
            request.POST._mutable = False

        # Check form is valid and if so call next method.
        if form.is_valid():
            if new_listing:
                add_new_game(request, form)
            else:
                update_game(request, form)

    # Render page
    return render(
        request,
        "staff/staff_game_management.html",
        {
            "form": GameManageForm(),
            "form_2": ConfirmGameDeleteForm(),
            "games": Game.objects.all(),
            "tags": Tag.objects.all(),
        },
    )


def delete_game(form: object):
    """
    Delete game from the database, and if a image was supplied it will delete
    the image from the server.

    Parameters:
    form : object
    """
    if form.data["game_delete_confirm"] == "delete" and form.data["id"]:
        item_id = form.data["id"]
        # Get current image for game
        game = get_object_or_404(Game, id=item_id)
        if game.image is not None:
            # Delete listing image from Cloudinary server
            uploader.destroy(game.image.public_id)
        # Delete game from database
        game.delete()


def add_new_game(request: object, form: object):
    """
    Saves new game to database, and if a image was supplied it will upload
    the image.

    Parameters:
    request : object.
    form : object
    """
    # Save form to database as a new game
    form.save()
    if request.FILES:
        game = get_object_or_404(Game, pk=form.data["id"])
        # Upload image
        new_image = uploader.upload(request.FILES["image"])
        game.image = new_image["url"]
        game.save()


def update_game(request: object, form: object):
    """
    Updates game to database, and if a image was supplied it will upload
    the image.

    Parameters:
    request : object.
    form : object
    """
    # Get correct game from database
    game = get_object_or_404(Game, pk=form.data["id"])
    # Update values
    game.name = form.data["name"]
    game.status = form.data["status"]
    game.slug = form.data["slug"]

    # Get tags selected from the form
    query = Q(id__in=form.cleaned_data["tags"])
    tags = Tag.objects.filter(query).all()

    # Update tags with tags selected from form
    game.tags.set(tags)

    # If game image already exists, delete from server and replace with
    # new image.
    if game.image is not None and request.FILES:
        # Delete old image from Cloudinary server
        uploader.destroy(game.image.public_id)

        # Get public ID
        txt = game.image.public_id
        public_id = txt.rsplit("/", 1)[1]
        # Upload new image
        new_image = uploader.upload(
            request.FILES["image"], public_id=public_id, overwrite=True
        )
        # Save new url to game object
        game.image = new_image["url"]

    # If game image does not exists, just upload.
    if game.image is None and request.FILES:
        # Upload new image
        new_image = uploader.upload(request.FILES["image"])
        game.image = new_image["url"]

    # Save game object
    game.save()


@staff_member_required
@login_required
def tag_management(request: object):
    """
    request.GET: Loads html page using render().

    request.POST: Processes adding, updating and deleting tags.

    Args:
        request (object): request data received from POST

    Returns:
        render: Loads html page
    """

    if request.method == "POST":
        # New listing flag - default to False
        new_listing = False

        # Let's see if the user is trying to delete a tag.
        if ConfirmTagDeleteForm(request.POST) and "tag_delete_confirm" in request.POST:
            form = ConfirmTagDeleteForm(request.POST)
            delete_tag(form)
            return redirect("tag_management")

        # Checking if updating a current tag
        elif request.POST["id"]:
            form = TagsManageForm(
                request.POST, instance=get_object_or_404(Tag, pk=request.POST["id"])
            )
            # New listing flag - False
            new_listing = False

        # Or if inputting a new tag
        else:
            form = TagsManageForm(request.POST)
            # New listing flag - True
            new_listing = True
            # Allow object to the edited
            request.POST._mutable = True
            # Get next ID and assign slug
            form.data["id"] = Tag.objects.order_by("-id").first().id + 1
            form.data["slug"] = "Tag-" + str(form.data["id"])
            # Restrict object from being edited
            request.POST._mutable = False

        # Check form is valid and if so call next method.
        if form.is_valid():
            if new_listing:
                add_new_tag(form)
            else:
                update_tag(form)

    # Render page
    return render(
        request,
        "staff/staff_tag_management.html",
        {
            "form": TagsManageForm(),
            "form_2": ConfirmTagDeleteForm(),
            "tags": Tag.objects.all(),
        },
    )


def delete_tag(form: object):
    """
    Delete tag from the database.

    Parameters:
    form : object
    """
    if form.data["tag_delete_confirm"] == "delete" and form.data["id"]:
        item_id = form.data["id"]
        # Get tag object
        tag = get_object_or_404(Tag, id=item_id)
        # Delete tag from database
        tag.delete()


def add_new_tag(form: object):
    """
    Saves new tag to database.

    Parameters:
    form : object
    """
    # Save form to database as a new tag
    form.save()


def update_tag(form: object):
    """
    Updates tag to database.

    Parameters:
    request : object.
    form : object
    """
    # Get correct tag from database
    tag = get_object_or_404(Tag, pk=form.data["id"])
    # Update values
    tag.name = form.data["name"]
    tag.slug = form.data["slug"]

    # Save tag object
    tag.save()


@staff_member_required
@login_required
def staff_user_management_search(request: object):
    """
    request.GET: Loads html page using render().

    request.POST: Processes updating and deleting user.

    Args:
        request (object): request data received from POST

    Returns:
        render(): Loads html page
    """

    if request.method == "POST":
        pass

    # Render page
    return render(
        request,
        "staff/staff_user_management_search.html",
        {

        },
    )

@staff_member_required
@login_required
def staff_user_management_user(request: object, _id: int):
    """
    request.GET: Loads html page using render().

    request.POST: Processes adding, updating and deleting user.

    Args:
        request (object): request data received from POST
        _id (int): Received user ID

    Returns:
        render(): Loads html page
    """
    user = get_object_or_404(CustomUser, id=_id)
    server_listings = ServerListing.objects.filter(
        owner=user.id).order_by('-created_on')

    if request.method == "POST":
        # Let's see if the user is trying to delete a user.
        if "delete_confirm" in request.POST:
            form = DeleteConfirmForm(request.POST)
            delete_user(form)
            return redirect("staff_user_management_search")

        else:
            form = UserForm(request.POST)
            update_user(form)
            return HttpResponse('Data Saved!')

    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in server_listings.values_list('id')]
    query = Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()

    # Pair images with server listing
    for index, value in enumerate(server_listings):
        # try to pair image with server listing, if image not available or does not
        # exist then set as None so a placeholder can be shown instead.
        try:
            image = images_queryset.get(listing_id=server_listings[index].id).image

            match images_queryset.get(listing_id=server_listings[index].id).status:
                case 0:
                    status = "Awaiting review"
                case 1:
                    status = "Approved"
                case 2:
                    status = "Rejected"
                case 3:
                    status = "Banned"

        except ObjectDoesNotExist:
            image = None
            status = None
        finally:
            server_listings[index].image_url = image
            server_listings[index].image_status = status

    # Render page
    return render(
        request,
        "staff/staff_user_management_user.html",
        {
            "form": UserForm(instance=user),
            "form_2": DeleteConfirmForm(),
            "server_listings": server_listings
        },
    )

def update_user(_form: dict):
    """
    Updates user to database.

    Parameters:
    request : object
    form : dict
    """
    # Get correct user from database
    user = get_object_or_404(CustomUser, pk=_form["id"])

    # Validate user inputs conform
    result = check_username(_form["username"])
    if not result['result']:
        return result

    result = check_email(_form["email"])
    if not result['result']:
        return result

    # Update values
    user.username = _form["username"]
    user.first_name = _form["first_name"]
    user.email = _form["email"]
    user.email_verified = _form["email_verified"]
    user.is_staff = _form["is_staff"]
    user.is_active = _form["is_active"]
    user.is_banned = _form["is_banned"]

    # Save user object
    try:
        user.save()
    except IntegrityError as e:
        print(e.args)
        if 'UNIQUE constraint failed: auth_user.username' in e.args:
            return { 'result': False, 'reason': "Username already taken"}
        if 'UNIQUE constraint failed: auth_user.email' in e.args:
            return { 'result': False, 'reason': "Email address already taken"}

    return { 'result': True, 'reason': "No problems"}


def delete_user(form: object):
    """
    Delete user from the database.

    Parameters:
    form : object
    """
    if form.data["delete_confirm"] == "delete" and form.data["id"]:
        item_id = form.data["id"]
        # Get user object
        user = get_object_or_404(CustomUser, id=item_id)
        # Delete user from database
        user.delete()


def check_username(username: str):
    """
    Checks username given conforms to rules

    Args:
        username (string): username given

    Returns:
        {result (bool), reason (string)}

    """

    if " " in username:
        return { 'result': False, 'reason': "No spaces allowed"}

    if len(username) < 5:
        return { 'result': False, 'reason': "Must be at least 5 characters long"}

    if len(username) > 20:
        return { 'result': False, 'reason': "Must be at 20 characters or less"}

    return { 'result': True, 'reason': ""}


def check_email(email):
    """
    Checks email address given conforms to rules

    Args:
        email (string): username given

    Returns:
        {result (bool), reason (string)}

    """
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat,email) is None:
        return { 'result': False, 'reason': "Email address not valid"}

    return { 'result': True, 'reason': ""}