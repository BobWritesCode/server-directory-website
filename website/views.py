from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
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
from datetime import timedelta, date
import json


from .constants import DAYS_TO_EXPIRE_IMAGE

from .forms import (
    ProfileForm, CreateServerListingForm, ConfirmAccountDeleteForm,
    SignupForm, UserUpdateEmailAddressForm, ConfirmServerListingDeleteForm,
    ImageForm
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

            if request.FILES:
                image = uploader.upload(request.FILES['image'])
                image_form.instance.image = image['url']

            form.instance.owner = request.user
            form.save()

            image_form.instance.user = request.user
            image_form.instance.listing = get_object_or_404(ServerListing, pk=form.instance.id)
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


    # Get images for server listings
    # Makes sure they are status 1: approved.
    _list = [x[0] for x in queryset.values_list('id')]
    query =  Q(listing_id__in=_list)
    images_queryset = Images.objects.filter(query).distinct()


    # Pair images with server listing
    for index, value in enumerate(queryset):
        # try to pair image with server listing, if image not available or does not
        # exist then set as None so a placeholder can be shown instead.
        try:
            image = images_queryset.get(listing_id=queryset[index].id).image

            match images_queryset.get(listing_id=queryset[index].id).status:
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
            queryset[index].image_url = image
            queryset[index].image_status = status


    form = ProfileForm(instance=request.user)
    form_2 = ConfirmAccountDeleteForm(instance=request.user)
    form_3 = UserUpdateEmailAddressForm(instance=request.user)
    form_4 = ConfirmServerListingDeleteForm(instance=request.user)

    # Get user bumped servers
    query = Q(user = request.user)
    bumps_queryset = Bumps.objects.filter(query)
    # Get server queryset based on users bumped servers
    query = Q(pk__in = bumps_queryset.values_list('listing_id'))
    server_listings_queryset = ServerListing.objects.filter(query)
    # Add server listing slug to bumps queryset
    for index, value in enumerate(bumps_queryset):
        bumps_queryset[index].url = server_listings_queryset.get(id=value.listing.id).slug
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
            'server_listing': queryset,
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
    print(request)
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

        return HttpResponse(json.dumps({'result': result}))


def ban_user(user_id):
    '''
    Prevents user login, rejects all images for deletion, unpublish listings.
    '''
    # Set user to is banned.
    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_banned = True
    user.save()

    # Unpublish all listings
    query = Q(owner_id = user_id)
    ServerListing.objects.filter(query).update(status=0)

    # Unpublish all images and set for deletion
    query = Q(user_id = user_id)
    image_expire = date.today() + timedelta(days = DAYS_TO_EXPIRE_IMAGE)
    Images.objects.filter(query).update(status = 3, expiry = image_expire)