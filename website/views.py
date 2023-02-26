"""
Contains vast majority of methods to run app
"""
from datetime import timedelta, date
import json
import operator
import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import mail
from django.db import IntegrityError
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404,  HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from cloudinary import uploader

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


def index(request: object):
    """
    Load index view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    games = Game.objects.filter(status=1).annotate(
        listing_count=Count('listing')).order_by('-listing_count')
    ctx = {
        'games': games,
        'tag_string': "0",
    }
    return render(request, "index.html", ctx)


def account_deleted(request: object):
    """
    Load account deleted view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "registration/account_deleted.html")


def signup_verify_email(request: object):
    """
    Load Signup verify view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "registration/signup_verify_email.html")


def email_address_verified(request: object):
    """
    Load email address verified view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "registration/email_address_verified.html")


def terms_and_conditions(request: object):
    """
    Load terms and conditions view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "terms_and_conditions.html")


def privacy_policy(request: object):
    """
    Load privacy policy view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "privacy_policy.html")


def contact_us(request: object):
    """
    Load contact us view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "contact_us.html")


def unauthorized(request: object):
    """
    Load unauthorized view.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
    return render(request, "unauthorized.html")


@login_required
@staff_member_required
def staff_account(request: object):
    """
    Load staff account view.

    Decorators:
        @login_required: User required to be logged in.
        @staff_member_required: Logged in user must be staff.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """
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
def staff_image_review(request: object, item_pk: int = None):
    """
    Load staff account view.

    Decorators:
        @login_required: User required to be logged in.
        @staff_member_required: Logged in user must be staff.

    Args:
        request (object): GET/POST request from user.
        item_pk (int): pk of image to load.

    Returns:
        render() (func): Loads the html page.
    """
    if request.method == 'POST':

        query = Q(status=0)
        image_count = Images.objects.filter(query).count()
        # If no image is currently waiting be approved,
        # then handle request.
        if image_count == 0:
            return redirect('staff_account')

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

    # Set status text based on image.status.
    match image.status:
        case 0:
            image.status_txt = "Awaiting approval"
        case 1:
            image.status_txt = "Approved"
        case 2:
            image.status_txt = "Rejected"
        case 3:
            image.status_txt = "Image rejected, user banned!"

    user = get_object_or_404(CustomUser, pk=image.user_id)
    listing = get_object_or_404(ServerListing, pk=image.listing_id)

    return render(
        request,
        "staff/staff_image_review.html",
        {
            'image': image,
            'user': user,
            'listing': listing,
        },
    )


@login_required
def server_create(request: object):
    """
    Create listing.

    Decorators:
        @login_required: User required to be logged in.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render() (func): Loads the html page.
    """

    if request.method == 'POST':

        form = CreateServerListingForm(request.POST)
        image_form = ImageForm(request.FILES)

        if form.is_valid() and image_form.is_valid():

            form.instance.owner = request.user
            form.save()

            if request.FILES:

                new_image = uploader.upload(
                    request.FILES['image'],
                    folder="server_directory/",
                    allowed_formats=['jpg', 'png', 'jpeg'],
                    format='jpg'
                    )
                image_form.instance.image = new_image['url']
                image_form.instance.public_id = new_image['public_id']
                image_form.instance.user = request.user
                image_form.instance.listing = get_object_or_404(
                    ServerListing, pk=form.instance.pk)
                image_form.instance.approved_by = None
                image_form.save()

        return redirect('my_account')

    return render(
        request,
        "server_create.html",
        {
            'form': CreateServerListingForm(),
            'image_form': ImageForm(),
            'tags': Tag.objects.all().order_by('name'),
        }
    )


@login_required
def server_edit(request: object, _pk: int):
    """
    Update listing.

    Decorators:
        @login_required: User required to be logged in.

    Args:
        request (object): GET/POST request from user.
        _pk (string): primary key for server that is being updated

    Returns:
        redirect (function): Unauthorized page
        redirect (function): My account page
        redirect (function): My account page
        render (function): Loads html page

    """
    item = get_object_or_404(ServerListing, pk=_pk)

    if (item.owner != request.user and not request.user.is_staff):
        return redirect("unauthorized")

    query = Q(serverlisting=item)
    selected_tags = Tag.objects.filter(query).order_by('name')

    if request.method == "POST":

        # Let's see if the user is trying to delete the listing.
        if "server_listing_delete_confirm" in request.POST:
            if request.POST["server_listing_delete_confirm"] == "delete":
                server_delete(request, item_pk=_pk)
                return redirect("my_account")

        # If user is trying to update the listing
        form = CreateServerListingForm(request.POST)
        image_form = ImageForm(request.FILES)

        if form.is_valid():

            image = Images.objects.filter(listing_id=_pk).first()

            # If there is a current listing image
            # and image trying to be saved.
            if image is not None and request.FILES:
                # Delete old image from Cloudinary server
                uploader.destroy(image.public_id)
                # Upload new imaged
                new_image = uploader.upload(
                    request.FILES['image'],
                    folder="server_directory/",
                    allowed_formats=['jpg', 'png', 'jpeg'],
                    format='jpg'
                    )

            # If no current listing image
            # and image trying to be saved.
            if image is None and request.FILES:
                # Upload new imaged
                new_image = uploader.upload(
                    request.FILES['image'],
                    folder="server_directory/",
                    allowed_formats=['jpg', 'png', 'jpeg'],
                    format='jpg'
                    )
                image = image_form.instance
                image.user = request.user
                image.listing = get_object_or_404(ServerListing, pk=_pk)

            # Save new image.
            if request.FILES:
                image.date_added = date.today()
                image.status = 0
                image.reviewed_by = None
                image.image = new_image['url']
                image.public_id = new_image['public_id']
                image.approved_by = None
                image.save()

            # Get tags selected from the form
            query = Q(id__in=form.cleaned_data["tags"])
            tags = Tag.objects.filter(query).all().order_by('name')

            item.title = form.data['title']
            item.tags.set(tags)
            item.short_description = form.data['short_description']
            item.long_description = form.data['long_description']
            item.status = form.data['status']
            item.discord = form.data['discord']
            item.tiktok = form.data['tiktok']
            item.save()
        return redirect("my_account")

    # Set status text based on image.status.
    try:
        # Get images for server listings
        # Makes sure they are status 1: approved.
        query = Q(listing_id=item.pk)
        listing_image = Images.objects.filter(query).first()

        match listing_image.status:
            case 0:
                listing_image.status_txt = "Awaiting approval"
            case 1:
                listing_image.status_txt = "Approved"
            case 2:
                listing_image.status_txt = "Rejected"
            case 3:
                listing_image.status_txt = "Image rejected, user banned!"
    except AttributeError:
        listing_image = None

    context = {
        "form": CreateServerListingForm(instance=item),
        "form_2": ConfirmServerListingDeleteForm(instance=item),
        "item": item,
        'image_form': ImageForm(),
        'listing_image': listing_image,
        'tags': Tag.objects.all().order_by('name'),
        'selected_tags': serializers.serialize('json', selected_tags),
    }
    return render(request, "server_edit.html", context)


@login_required
def server_delete(request: object, item_pk: int):
    """
    Delete listing.

    Decorators:
        @login_required: User required to be logged in.

    Args:
        request (object): GET/POST request from user.
        item_pk (string): primary key for server that is being updated

    Returns:
        redirect (function): Loads html page

    """
    item = get_object_or_404(ServerListing, pk=item_pk)
    image = Images.objects.filter(listing_id=item_pk).first()
    if image is not None:
        # Delete listing image from Cloudinary server
        uploader.destroy(image.public_id)
    item.delete()
    return redirect('my_account')


@login_required
def my_account(request: object):
    """
    My account view.

    Decorators:
        @login_required: User required to be logged in.

    Args:
        request (object): GET/POST request from user.

    Returns:
        redirect (function): Unauthorized page
        redirect (function): My account page
        redirect (function): My account page
        render (function): Loads html page
    """

    if request.method == 'POST':

        # Let's see if the user is trying to delete a listing.
        if 'server_listing_delete_confirm' in request.POST:
            form_4 = ConfirmServerListingDeleteForm(request.POST)

            if request.POST['server_listing_delete_confirm'] == 'delete':
                item_pk = form_4.data['itemID']

                # Get current image for listing
                item = get_object_or_404(ServerListing, pk=item_pk)
                image = Images.objects.filter(listing_id=item_pk).first()
                if image is not None:
                    # Delete listing image from Cloudinary server
                    uploader.destroy(image.public_id)

                # Delete server listing from database
                item.delete()

                return redirect("my_account")

        # Let's see if the user is trying to delete there account.
        if 'account_delete_confirm' in request.POST:
            form_2 = ConfirmAccountDeleteForm(request.POST)
            # Check if user has typed the correct phrase and hit submit
            if request.POST['account_delete_confirm'] == 'remove':
                CustomUser.objects.get(pk=request.user.pk).delete()
                return redirect(to='account_deleted')

    username = request.user
    listings = ServerListing.objects.filter(
        owner=username).order_by('-created_on')
    num_of_listings = listings.count()

    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in listings.values_list('id')]
    query = Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()

    # Pair images with server listing
    for key, value in enumerate(listings):
        # try to pair image with server listing, if image not available
        # or does not exist then set as None so a placeholder can be
        # shown instead.
        try:
            image = images_queryset.get(listing_id=value.pk).image
            match images_queryset.get(listing_id=value.pk).status:
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

        listings[key].image_url = image
        listings[key].image_status = status
        listings[key].bump_count = value.bump_counter()

    form = ProfileForm(instance=request.user)
    form_2 = ConfirmAccountDeleteForm(instance=request.user)
    email_form = UserUpdateEmailAddressForm()
    form_4 = ConfirmServerListingDeleteForm(instance=request.user)

    # Get user bumped servers
    query = Q(user=request.user)
    bumps_queryset = Bumps.objects.filter(query)
    # Get server queryset based on users bumped servers
    query = Q(pk__in=bumps_queryset.values_list('listing_id'))
    server_listings_queryset = ServerListing.objects.filter(query)
    # Add server listing slug to bumps queryset
    for key, value in enumerate(bumps_queryset):
        bumps_queryset[key].url = server_listings_queryset.get(
            id=value.listing.pk).slug
    # Calculate how many bumps the user has left to use
    bumps_left = 5 - len(bumps_queryset)

    return render(
        request,
        'registration/my_account.html',
        {
            'form': form,
            'form_2': form_2,
            'email_form': email_form,
            'form_4': form_4,
            'server_listings': listings,
            'num_of_listings': num_of_listings,
            'bumps': bumps_queryset,
            'bumps_left': bumps_left,
        }
    )


def sign_up_view(request):
    """
    GET: Loads sign up view
    POST: Attempts to create a new user, unless there is an error
    then displays error to the user.

    Args:
        request (object): GET/POST request from user.

    Returns:
        redirect (function): Email verification view.
        render (function): Loads view.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # Check user has completed form as required.
        if form.is_valid():
            # Original code before modifications, check ReadMe:
            # https://shafikshaon.medium.com/
            # user-registration-with-email-verification-in-django-8aeff5ce498d
            # Save new user to database.

            try:
                user = form.save()
                send_email_verification(request, user)
                return redirect('signup_verify_email')
            except ValidationError as err:
                for field, errors in err.message_dict.items():
                    form.add_error(field, errors)
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request: object, uidb64, token):
    """
    Activate user account after they have they visited the link in the
    email address verification, sent to the user by email.

    Args:
        request (object): GET/POST request from user.
        uidb64 ():
        token ():

    Returns:
        redirect (function): Email address verified view.
        HttpResponse (class): Activation link is invalid.
    """
    # Original code:
    # https://shafikshaon.medium.com/
    # user-registration-with-email-verification-in-django-8aeff5ce498d
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        return redirect('email_address_verified')
    return HttpResponse('Activation link is invalid!')


def listings_view(request: object, slug: str, tag_string: str = ""):
    """
    Loads listings view.

    Args:
        request (object): GET/POST request from user.
        slug (str): Keeps track of user's selected tags.
        tag_string (str): Keeps track of user's selected tags.

    Returns:
        render(): Loads html page.

    """
    # Get only the tags linked to a game.
    game = get_object_or_404(Game, slug=slug)
    tags = game.tags.all()

    query = Q(status=1) & Q(game=game)
    listings = ServerListing.objects.filter(query).distinct()

    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in listings.values_list('id')]
    query = Q(status=1) & Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()

    # Get user bumps
    user_bumps_queryset = get_user_bumps(request)

    # Create and empty list then append all tags into that list.
    all_tags_for_game = []
    for tag in tags:
        all_tags_for_game.append([tag.pk, tag.name])

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
            listings = listings.filter(tags__name=value)

        # Use list comprehension to remove selected tags from all
        # available tags
        tags = [x for x in game.tags.all() if x.name not in selected_tags]

        tags.sort(key=operator.attrgetter('name'))
        selected_tags.sort()

    else:
        # If tag_string empty then create empty list
        selected_tags = []
        # Get all available tags for game selected
        tags = game.tags.all().order_by('name')

    # Now now longer required to to stay a queryset, convert to list
    # and reorder by bump count.
    listings = sorted(listings.all(), key=lambda a: a.bump_counter(),
                      reverse=True)

    # Pair images with server listing.
    # And add bump count.
    for key, value in enumerate(listings):
        # try to paid image with server listing, if image not available or
        # does not exist then set as None so a placeholder can be
        # shown instead.
        try:
            image = images_queryset.get(listing_id=value.pk).image
        except ObjectDoesNotExist:
            image = None

        listings[key].image_url = image
        listings[key].bump_count = value.bump_counter()

    return render(
        request,
        "listings.html",
        {
            "listings": listings,
            "bumps_queryset": user_bumps_queryset,
            "selected_tags": selected_tags,
            "tags": tags,
            "tag_string": tag_string,
            "slug": slug,
        },
    )


@login_required
def get_user_bumps(request: object):
    '''
    Returns a list of user's current bumps.

    Decorators:
        @login_required: User required to be logged in.

    Parameters:
        request (Any): The server request

    Returns:
        bumps_queryset (list): List of user's active bumps
    '''
    query = Q(user=request.user)
    bumps_queryset = Bumps.objects.filter(query).values_list('listing_id')
    _list = [x[0] for x in bumps_queryset]
    return _list


def listing_view(request: object, slug: str):
    """
    Loads listing detail view.

    Args:
        request (object): GET/POST request from user.
        slug (str): Which game to load.

    Returns:
        render(): Loads html page.
    """
    # Get correct listing, check if approved.
    listing = get_object_or_404(ServerListing, status=1, slug=slug)

    if request.user.is_staff:
        listing_owner = listing.owner
    else:
        listing_owner = None

    # Get user bumps.
    bumps_queryset = get_user_bumps(request)

    # Get listing approved images.
    query = Q(status=1) & Q(listing_id=listing.id)
    images = Images.objects.filter(query).distinct()

    listing.bump_count = listing.bump_counter()

    return render(
        request,
        "listing.html",
        {
            "images": images,
            "listing": listing,
            "bumps_queryset": bumps_queryset,
            "listing_owner": listing_owner,
        },
    )


@require_POST
def send_email_verification(request: object, user: object):
    '''
    Send email address verification to user.

    Decorators:
        @require_POST: Allow POST only.

    Parameters:
        request (object): GET/POST request from user.
        user (object): Target user model object
    '''
    current_site = get_current_site(request)
    message = render_to_string('email_templates/verify_email_address.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)})
    # Send email to user.
    mail.send_mail(
        subject='Verify your email address.',
        message=message,
        from_email='contact@warwickhart.com',
        recipient_list=[user.email])

    return HttpResponse('send_email_verification success.')


@login_required
@require_POST
def bump_server(request: object):
    """
    Add 1 bump to server if already not bumped by user

    Decorators:
        @login_required: User required to be logged in
        @require_POST: Allow POST only.

    Parameters:
        request (object): POST request from user.

    Returns:
        HttpResponse(json({}'result': number of bumps (int)}))
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = int(body['server_id'])

    # Get server listing object
    listing = get_object_or_404(ServerListing, id=content)

    # Get user bumps
    bumps_queryset = get_user_bumps(request)

    # Check if this server already bumped by user
    if content in bumps_queryset:
        return HttpResponse(
            json.dumps({'result': len(bumps_queryset)}))

    # Check user has not already bumped max server amount
    if len(bumps_queryset) > 4:
        return HttpResponse(
            json.dumps({'result': len(bumps_queryset)}))

    # Add 1 to bump count for frontend
    bumps_queryset_len = len(bumps_queryset) + 1

    # Create a row to table and save
    bump = Bumps.objects.create(user=request.user, listing=listing)
    bump.save()
    return HttpResponse(
        json.dumps({'result': int(bumps_queryset_len)}))


@login_required
@require_POST
def call_server(request: object):
    """
    Method for frontend to call backend with a request.

    Decorators:
        @login_required: User required to be logged in
        @require_POST: Allow POST only.

    Parameters:
        request (object): GET/POST request from user.

    Returns:
        HttpResponse(json.dumps({'result': result}))
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['args']

    match content[0]:
        case 'image_approval_approve':
            if request.user.is_staff:
                item = get_object_or_404(Images, pk=content[1])
                item.status = 1
                item.expiry = None
                item.reviewed_by = request.user
                item.save()
                result = {
                    'success': True,
                    'text': "Approved"
                }
            else:
                return render(request, "unauthorized.html")

        case 'image_approval_reject':
            if request.user.is_staff:
                item = get_object_or_404(Images, pk=content[1])
                item.status = 2
                item.expiry = date.today() + timedelta(
                    days=DAYS_TO_EXPIRE_IMAGE)
                item.reviewed_by = request.user
                item.save()
                result = {
                    'success': True,
                    'text': "Rejected"
                }
            else:
                return render(request, "unauthorized.html")

        case 'image_approval_ban':
            if request.user.is_staff:
                item = get_object_or_404(Images, pk=content[1])
                item.status = 3
                item.expiry = date.today() + timedelta(
                    days=DAYS_TO_EXPIRE_IMAGE)
                item.reviewed_by = request.user
                item.save()
                ban_user(request, item.user_id)
                result = {
                    'success': True,
                    'text': "Rejected and user banned"
                }
            else:
                return render(request, "unauthorized.html")

        case 'get_game_details':
            if request.user.is_staff:
                game = get_object_or_404(Game, id=content[1])
                query = Q(game=content[1])
                tags = Tag.objects.filter(query).order_by('name')
                result = {
                    'success': True,
                    'game': game.to_json(),
                    'game_tags': serializers.serialize('json', tags),
                }
            else:
                return render(request, "unauthorized.html")

        case 'get_tag_details':
            if request.user.is_staff:
                tag = get_object_or_404(Tag, pk=content[1])
                result = {
                    'success': True,
                    'tag': tag.to_json(),
                }
            else:
                return render(request, "unauthorized.html")

        case 'search_users_username':
            if request.user.is_staff:
                query = Q(username__contains=content[1])
                # Limited to first 100 results.
                users = CustomUser.objects.filter(query)[:100]
                result = {
                    'success': True,
                    'users': serializers.serialize('json', users),
                }
            else:
                return render(request, "unauthorized.html")

        case 'search_users_email':
            if request.user.is_staff:
                query = Q(email__contains=content[1])
                # Limited to first 100 results.
                users = CustomUser.objects.filter(query)[:100]
                result = {
                    'success': True,
                    'users': serializers.serialize('json', users),
                }
            else:
                return render(request, "unauthorized.html")

        case 'search_users_id':
            if request.user.is_staff:
                query = Q(id__contains=int(content[1]))
                # Limited to first 100 results.
                users = CustomUser.objects.filter(query)[:100]
                result = {
                    'success': True,
                    'users': serializers.serialize('json', users),
                }
            else:
                return render(request, "unauthorized.html")

        case 'update_email':
            email1 = str(content[1]['email1']).lower()
            email2 = str(content[1]['email2']).lower()
            success = update_email(request, [email1, email2])
            result = {
                'success': success['result'],
                'reason': success['reason']
            }

        case 'get_game_tags':
            if request.user:
                game = get_object_or_404(Game, id=content[1])
                tags = game.tags.all().order_by('name')
                all_tags_for_game = []
                for tag in tags:
                    all_tags_for_game.append([tag.pk, tag.name])
                result = {
                    'success': "tags",
                    'reason': all_tags_for_game
                }
            else:
                return render(request, "unauthorized.html")

    return HttpResponse(json.dumps({'result': result}))


@staff_member_required
@login_required
def ban_user(request: object, _id: int):
    """
    Bans user and prevents user login, rejects all images for deletion,
    unpublish listings.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Parameters:
        request (object): GET/POST request from user.#
        _id (int): Target user to be banned.
    """
    # Get target user.
    user = get_object_or_404(CustomUser, pk=_id)

    # Delete all current user active sessions.
    Session.objects.filter(expire_date__gte=timezone.now(),
                           session_key__contains=user.pk).delete()

    # Flag user as banned.
    user.is_banned = True
    user.save()

    # Unpublish all listings
    query = Q(owner_id=_id)
    ServerListing.objects.filter(query).update(status=0)

    # Unpublish all images and set for deletion
    query = Q(user_id=_id)
    image_expire = date.today() + timedelta(days=DAYS_TO_EXPIRE_IMAGE)
    Images.objects.filter(query).update(status=3, expiry=image_expire)


@staff_member_required
@login_required
def unban_user(request: object, _id: int):
    """
    Unbans target user.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Parameters:
        request (object): GET/POST request from user.#
        _id (int): Target user to be banned.
    """
    # Get target user.
    user = get_object_or_404(CustomUser, id=_id)
    user.is_banned = False
    user.save()

    # Un-expire all images
    query = Q(user_id=_id)
    Images.objects.filter(query).update(status=0, expiry=None)

    return HttpResponse(f'User unbanned: {_id}')


def login_view(request: object):
    """
    Login-view and process login.

    Args:
        request (object): GET/POST request from user..

    Returns:
        render(): Loads html page.
    """
    error_message = None

    # If user already logged in, just direct them to My Account page.
    if request.user.is_authenticated:
        return redirect("my_account")

    if request.method == 'POST':
        # Get from request user input.
        email = request.POST['email']
        password = request.POST['password']
        # Check credentials are found and a match.
        user = authenticate(email=email, password=password)
        if user is None:
            # ERROR: User not found, or password mismatch.
            error_message = (
                "Either user does not exist or password does not "
                "match account."
            )
        else:
            # Check if user is banned.
            if user.is_banned:
                # ERROR: User account has been flagged as banned.
                error_message = "This account is banned."
                user = None
            # All being okay, log user in.
            else:
                login(request, user)
                return redirect("my_account")

    return render(
        request,
        "registration/login.html",
        {
            "form": LoginForm(),
            "error_message": error_message,
        },
    )


@staff_member_required
@login_required
def game_management(request: object):
    """
    Updates, adds or deletes games.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render: Loads html page
    """
    if request.method == "POST":
        # User is trying to delete a game.
        if "game_delete_confirm" in request.POST:
            delete_game(request.POST)
        # User is trying to update a game.
        elif request.POST["id"]:
            update_game(data=request.POST, files=request.FILES)
        # Uer is trying to add a new game.
        else:
            add_new_game(data=request.POST, files=request.FILES)
    # Render page
    return render(
        request,
        "staff/staff_game_management.html",
        {
            "form": GameManageForm(),
            "form_2": ConfirmGameDeleteForm(),
            "games": Game.objects.all().order_by('name'),
            "tags": Tag.objects.all().order_by('name'),
        },
    )


def delete_game(data: object):
    """
    Deletes game from the database.

    Args:
        form (object): Provides data to delete game.

    Returns:
        HttpResponse (class): Feedback result of codeblock.
    """
    form = ConfirmGameDeleteForm(data)
    if form.data["game_delete_confirm"] == "delete" and form.data["itemID"]:
        item_id = form.data["itemID"]
        # Get current image for game
        game = get_object_or_404(Game, id=item_id)
        if game.image is not None:
            # Delete listing image from Cloudinary server
            uploader.destroy(game.image.public_id)
        # Delete game from database
        game.delete()
        return HttpResponse('Success - Game deleted.')
    return HttpResponse('Failed - No game deleted.')


def add_new_game(data: object, files: object = None):
    """
    Adds new game to the database.

    Args:
        data (object): Provides data for new game.
        files (object): Image file(s)

    Returns:
        HttpResponse (class): Feedback result of codeblock.

    """
    form = GameManageForm(data)
    if form.is_valid():
        # Save form to database as a new game
        game = form.save()
        if files:
            # Upload image
            new_image = uploader.upload(
                files["image"],
                folder="server_directory/",
                allowed_formats=['jpg', 'png', 'jpeg'],
                format='jpg'
                )
            game.image = new_image["url"]
            game.save()
            return HttpResponse('New game added with image.')
        return HttpResponse('New game added with no image.')
    return HttpResponse('Failed to add new game.')


def update_game(data: object, files: object = {}):
    """
    Updates game in the database.

    Args:
        data (object): Provides data to update game.
        files (object): Image file(s)

    Returns:
        HttpResponse (class): Feedback result of codeblock.

    """

    game = get_object_or_404(Game, pk=data["id"])
    form = GameManageForm(data=data, instance=game)

    if form.is_valid():
        # Get correct game from database
        game = get_object_or_404(Game, pk=data["id"])
        # Update values
        game.name = data["name"]
        game.status = data["status"]
        game.slug = data["slug"]

        # Get tags selected from the form
        query = Q(id__in=form.cleaned_data["tags"])
        tags = Tag.objects.filter(query).all().order_by('name')

        # Update tags with tags selected from form
        game.tags.set(tags)

        # If game image already exists, delete from server and replace with
        # new image.
        if game.image is not None and files:
            # Delete old image from Cloudinary server
            uploader.destroy(game.image.public_id)

            # Get public ID
            txt = game.image.public_id
            public_id = txt.rsplit("/", 1)[1]
            # Upload new image
            new_image = uploader.upload(
                files["image"],
                public_id=public_id,
                overwrite=True,
                folder="server_directory/",
                allowed_formats=['jpg', 'png', 'jpeg'],
                format='jpg'
            )
            # Save new url to game object
            game.image = new_image["url"]

        # If game image does not exists, just upload.
        if game.image is None and files:
            # Upload new image
            new_image = uploader.upload(
                files["image"],
                folder="server_directory/",
                allowed_formats=['jpg', 'png', 'jpeg'],
                format='jpg'
                )
            game.image = new_image["url"]

        # Save game object
        game.save()
        return HttpResponse('Success - Game updated.')
    return HttpResponse('Failed - Game not updated.')


@staff_member_required
@login_required
def tag_management(request: object):
    """
    Updates, adds or deletes tags.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render (function): Loads html page
    """
    if request.method == "POST":

        # Let's see if the user is trying to delete a tag.
        if (
            ConfirmTagDeleteForm(request.POST)
            and "tag_delete_confirm" in request.POST
        ):
            form = ConfirmTagDeleteForm(request.POST)
            delete_tag(form)
            return redirect("tag_management")

        # Checking if updating a current tag
        elif request.POST["id"]:
            form = TagsManageForm(
                request.POST, instance=get_object_or_404(
                    Tag, pk=request.POST["id"])
            )
            update_tag(form)

        # Or if inputting a new tag
        else:
            form = TagsManageForm(request.POST)
            if form.is_valid():
                form_data = form.data.copy()
                # form_data['id'] = Tag.objects.order_by("-id").first().id + 1
                add_new_tag(TagsManageForm(form_data))

    # Render page
    return render(
        request,
        "staff/staff_tag_management.html",
        {
            "form": TagsManageForm(),
            "form_2": ConfirmTagDeleteForm(),
            "tags": Tag.objects.all().order_by('name'),
        },
    )


def delete_tag(form: object):
    """
    Delete tag from the database.

    Args:
        form (object): Data used to delete tag.
    """
    if form.data["tag_delete_confirm"] == "delete" and form.data["itemID"]:
        item_id = form.data["itemID"]
        # Get tag object
        tag = get_object_or_404(Tag, id=item_id)
        # Delete tag from database
        tag.delete()


def add_new_tag(form: object):
    """
    Saves new tag to database.

    Args:
        form (object): Data used to add tag.
    """
    # Save form to database as a new tag
    form.save()


def update_tag(form: object):
    """
    Update tag in database.

    Args:
        form (object): Data used to update tag.
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
    View to search for a member.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Args:
        request (object): GET/POST request from user.

    Returns:
        render(function): Loads html page
    """
    # Render page
    return render(
        request,
        "staff/staff_user_management_search.html",
        {},
    )


@staff_member_required
@login_required
def staff_user_management_user(request: object, _id: int):
    """
    Loads target user staff view account page of user.

    Decorators:
        @login_required: User required to be logged in
        @staff_member_required: Logged in user must be staff.

    Args:
        request (object): GET/POST request from user.
        _id (int): Target user ID.

    Returns:
        render (function): Loads html page
    """
    user = get_object_or_404(CustomUser, id=_id)
    listings = ServerListing.objects.filter(
        owner=user.pk).order_by('-created_on')

    form = UserForm(instance=user)

    # Let's see if the user is trying to update target user.
    if "user_management_save" in request.POST:
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"].lower()
            user.is_active = "is_active" in request.POST
            try:
                user.save()
                return redirect(
                    "staff_user_management_user", _id=request.POST['id'])
            except ValidationError as err:
                for field, errors in err.message_dict.items():
                    form.add_error(field, errors)

    # Let's see if the user is trying to delete target user.
    if "delete_confirm" in request.POST:
        form = DeleteConfirmForm(request.POST)
        delete_user(request, form)
        return redirect("staff_user_management_search")

    # Let's see if the user is trying to ban target user.
    if "ban_confirm" in request.POST:
        _id = request.POST['id']
        ban_user(request, _id)
        return redirect(
            "staff_user_management_user", _id=request.POST['id']
            )

    # Let's see if the user is trying to unban target user.
    if "unban" in request.POST:
        _id = request.POST['id']
        unban_user(request, _id)
        return redirect(
            "staff_user_management_user", _id=request.POST['id']
            )

    # Let's see if the user is trying to delete a listing of the
    # target user.
    if "delete_listing_confirm" in request.POST:
        # Let's see if the user is trying to delete the listing.
        if request.POST["delete_listing_confirm"] == "delete":
            item = get_object_or_404(ServerListing, id=request.POST['id'])
            item.delete()
            return redirect(
                "staff_user_management_user", _id=request.POST['id']
                )

    # Let's see if the user is trying to send a email verification
    # to the target user.
    if "email-verify" in request.POST:
        user.email_verified = False
        user.save()
        # Send email verification to the user
        send_email_verification(request, user)
        return redirect(
            "staff_user_management_user", _id=request.POST['id']
            )

    # Let's see if the user is trying to assign the target user
    # as a staff member.
    if "promote" in request.POST:
        promote_user_to_staff(request, request.POST['id'])
        return redirect(
            "staff_user_management_user", _id=request.POST['id']
            )

    # Let's see if the user is trying to resign the target user
    # as a staff member.
    if "demote" in request.POST:
        demote_user_from_staff(request, request.POST['id'])
        return redirect(
            "staff_user_management_user", _id=request.POST['id']
            )

    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in listings.values_list('id')]
    query = Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()

    # Pair images with server listing
    # And add bump count.
    for key, value in enumerate(listings):
        # try to pair image with server listing, if image not
        # available or does not exist then set as None so a placeholder
        # can be shown instead.
        try:
            image = images_queryset.get(listing_id=value.pk).image

            match images_queryset.get(listing_id=value.pk).status:
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

        listings[key].image_url = image
        listings[key].image_status = status
        # Adding bump count
        listings[key].bump_count = value.bump_counter()

    # Render page
    return render(
        request,
        "staff/staff_user_management_user.html",
        {
            "form": form,
            "form_2": DeleteConfirmForm(),
            "server_listings": listings
        },
    )


def promote_user_to_staff(request: object, target_id: int):
    """
    Promotes target user to staff member.

    Args:
        request (object): GET/POST request from user.
        target_id (int): Target user ID.
    """
    # Check request user has correct level before proceeding
    if request.user.is_superuser:
        # Get target user object.
        user = get_object_or_404(CustomUser, id=target_id)
        # Change flag.
        user.is_staff = True
        # Save user.
        user.save()


def demote_user_from_staff(request: object, target_id: int):
    """
    Demote target user as staff member.

    Args:
        request (object): GET/POST request from user.
        target_id (int): Target user ID.
    """
    # Check request user has correct level before proceeding
    if request.user.is_superuser:
        # Get target user object.
        user = get_object_or_404(CustomUser, id=target_id)
        # Change flag.
        user.is_staff = False
        # Save user.
        user.save()


def delete_user(request: object, form: object):
    """
    Delete target user from database.

    Args:
        request (object): GET/POST request from user.
        form (object): Data to delete user.
    """
    if form.data["delete_confirm"] == "delete" and form.data["id"]:
        item_id = form.data["id"]
        # Get user object
        user = get_object_or_404(CustomUser, id=item_id)
        if user.is_superuser and not request.user.is_superuser:
            # Delete user from database
            user.delete()


def check_username(username: str):
    """
    Checks username given conforms to rules.

    Args:
        username (string): Username given.

    Returns:
        {result (bool), reason (string)}

    """
    if " " in username:
        return {'result': False,
                'reason': "No spaces allowed"}
    if len(username) < 5:
        return {'result': False,
                'reason': "Must be at least 5 characters long"}
    if len(username) > 20:
        return {'result': False,
                'reason': "Must be at 20 characters or less"}
    return {'result': True,
            'reason': ""}


def check_email(email: str):
    """
    Checks email address given conforms to rules.

    Args:
        email (string): Username given.

    Returns:
        {result (bool), reason (string)}
    """
    pat = (
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#"
        "#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9"
        r"-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        )
    if re.match(pat, email) is None:
        return {'result': False, 'reason': "Email address not valid"}
    return {'result': True, 'reason': ""}


def update_email(request: object, _list: list):
    """
    Update user email after checking it conforms.

    Args:
        request (object): GET/POST request from user.
        _list (list): List with email address 1 and 2, must match.

    Returns:
        {result (bool), reason (string)}

    """
    result = check_email(_list[0])
    if not result['result']:
        return result

    if _list[0] != _list[1]:
        return {'result': False, 'reason': "Does not match"}

    # Get correct user from database
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    user.email = _list[0]
    user.email_verified = False
    # Save user object
    try:
        user.save()
    except IntegrityError as err:
        if 'UNIQUE constraint failed: auth_user.email' in err.args:
            return {'result': False, 'reason': "Email address already taken"}
    except ValidationError as e:
        for errors in e.message_dict.items():
            return {'result': False, 'reason': errors[1]}

    # Send verification email to the user.
    send_email_verification(request, user)

    return {'result': True, 'reason': ""}
