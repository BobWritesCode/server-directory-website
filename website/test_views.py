'''Tests for views.py'''

import json
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image as PILImage
from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
from django.http import HttpResponse
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client, RequestFactory
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser, Tag, Game, ServerListing, Images, Bumps
from .forms import (CreateServerListingForm, SignupForm,
                    GameManageForm)
from .views import (send_email_verification, delete_game,
                    add_new_game, update_game, update_email)


def create_user(num: str):
    '''Create test user'''
    return CustomUser.objects.create(
        username=f'T_User_{num}',
        password=f'TPass_{num}',
        email=f'{num}@d8sf87sdf9sd.com',
        email_verified=True,
        is_active=True,
        is_staff=False)


def create_user_staff(num: int):
    '''Create test staff user'''
    return CustomUser.objects.create(
        username=f'T_Staff_User_{num}',
        password=f'TPass_{num}',
        email=f't_staff_user_{num}@email34232343.com',
        email_verified=True,
        is_active=True,
        is_staff=True)


def create_user_super(num: int):
    '''Create test staff user'''
    return CustomUser.objects.create(
        username=f'T_Staff_User_{num}',
        password=f'TPass_{num}',
        email=f't_staff_user_{num}@email34232343.com',
        email_verified=True,
        is_active=True,
        is_staff=True,
        is_superuser=True)


def create_tag(num: int):
    '''Create test tag'''
    return Tag.objects.create(name=f'{num}', slug=f'{num}')


def create_game(num: int, placeholder: bool = False):
    '''Create test game, adds latest tag automatically'''
    obj = Game.objects.create(
        name=f'{num}',
        slug=f'{num}',
        image='placeholder' if placeholder else None,
        status=1)
    # add created cls.tag to game.
    obj.tags.set([Tag.objects.all().last()])
    return obj


def create_listing(num: int, user: object, game: object, tags: list):
    '''Create test listing'''
    obj = ServerListing.objects.create(
        game=game,
        owner=user,
        title=f'{num}',
        short_description='a' * 150,
        long_description='a' * 200,
        status=1,
        discord=f'{num}',
        tiktok=f'{num}')
    obj.tags.set(tags)
    return obj


def create_image(num: int, user: object, listing: object, status: int = 1):
    '''Create test image'''
    return Images.objects.create(
        user=user,
        listing=listing,
        status=status,
        public_id=num)


def create_bump(user: object, listing: object):
    '''Create test bump'''
    return Bumps.objects.create(
        user=user,
        listing=listing,)


def create_image_obj():
    '''Create an image object'''
    io = BytesIO()
    image = PILImage.new("RGB", (1, 1), (255, 255, 255))
    image.save(io, format="JPEG")
    image_file = InMemoryUploadedFile(
        io, 'image', 'image.jpg',
        "image/jpeg", io.getbuffer().nbytes, None)
    image_file.seek(0)
    return image_file


class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(678234)
        cls.staff_user = create_user_staff(478328904)
        cls.tag = create_tag(783423423)
        cls.game = create_game(893494)
        cls.game.tags.set([cls.tag])
        cls.server_listing = create_listing(
            num=738453824, user=cls.user, game=cls.game, tags=[cls.tag])

    @classmethod
    def tearDownClass(cls):
        cls.server_listing.delete()
        cls.game.delete()
        cls.tag.delete()
        cls.staff_user.delete()
        cls.user.delete()

    def test_index(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'index.html'
        )

    def test_account_deleted(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('account_deleted'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/account_deleted.html'
        )

    def test_signup_verify_email(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('signup_verify_email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/signup_verify_email.html'
        )

    def test_email_address_verified(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('email_address_verified'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/email_address_verified.html'
        )

    def test_terms_and_conditions(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('terms_and_conditions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'terms_and_conditions.html'
        )

    def test_privacy_policy(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'privacy_policy.html'
        )

    def test_contact_us(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'contact_us.html'
        )

    def test_unauthorized(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('unauthorized'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'unauthorized.html'
        )

    def test_staff_account(self):
        '''Test to check getting correct page'''
        # Unregistered user
        self.client.logout()
        response = self.client.get(reverse('staff_account'))
        self.assertEqual(response.status_code, 302)

        # Registered, non-staff user
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('staff_account'))
        self.assertEqual(response.status_code, 302)

        # Registered, staff user.
        self.client.force_login(user=self.staff_user)
        response = self.client.get(reverse('staff_account'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            'staff/staff_account.html'
        )


class TestStaffImageReview(TestCase):
    '''Tests for staff_image_review view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(345436)
        cls.staff_user = create_user_staff(2131214)
        cls.tag = create_tag(897686545)
        cls.game = create_game(62348973)
        cls.server_listing = ServerListing.objects.create(
            game=cls.game,
            owner=cls.user,
            status=1,
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.test_image = Images.objects.create(
            user=self.user,
            listing=self.server_listing,
            status=1)

    def tearDown(self):
        self.test_image.delete()

    def test_page_renders_only_when_user_is_staff(self):
        '''Test page render when user is staff otherwise redirect'''

        # Set all images to approved so there are no images to review.
        Images.objects.all().update(status=1)

        # Unregistered user
        response = self.client.get(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 302)

        # Registered, non-staff user
        self.client.force_login(self.user)
        response = self.client.get(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 302)

        # Registered, staff user.
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('staff_image_review'))
        # Redirect to staff page as no images to be reviewed.
        self.assertEqual(response.status_code, 302)

        # Change 1 image to status 0
        self.test_image.status = 0
        self.test_image.save()
        # Reload page
        response = self.client.get(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            'staff/staff_image_review.html')

    def test_staff_image_review_status_text(self):
        '''Check image status text'''
        self.client.force_login(self.staff_user)
        self.test_image.status = 0
        self.test_image.save()
        response = self.client.get(
            f'/staff_image_review/{self.test_image.pk}')
        self.assertContains(response, 'Awaiting approval')

        self.test_image.status = 1
        self.test_image.save()
        response = self.client.get(
            f'/staff_image_review/{self.test_image.pk}')
        self.assertContains(response, 'Approved')

        self.test_image.status = 2
        self.test_image.save()
        response = self.client.get(
            f'/staff_image_review/{self.test_image.pk}')
        self.assertContains(response, 'Rejected')

        self.test_image.status = 3
        self.test_image.save()
        response = self.client.get(
            f'/staff_image_review/{self.test_image.pk}')
        self.assertContains(response, 'Image rejected, user banned!')

    def test_staff_image_review_invalid_pk(self):
        '''Test if try to load a page with invalid item pk'''
        self.client.force_login(self.staff_user)
        self.test_image.status = 0
        self.test_image.save()
        invalid_id = Images.objects.order_by('-id').first().id + 1
        response = self.client.get(
            f'/staff_image_review/{invalid_id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('staff_account'))

    def test_post_no_images_too_review(self):
        '''Test POST with no images to review'''
        self.client.force_login(self.staff_user)
        Images.objects.all().update(status=1)
        response = self.client.post(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('staff_account'))

    def test_post_images_too_review(self):
        '''Test once POST and images still to be reviewed'''
        self.client.force_login(self.staff_user)
        self.test_image.status = 0
        self.test_image.save()
        response = self.client.post(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 200)


class TestServerCreate(TestCase):
    '''Tests server_create view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(763543345)
        cls.staff_user = create_user_staff(43252435)
        cls.tag = create_tag(23435435)
        cls.game = create_game(234235654)
        cls.listing = create_listing(
            num=654643345, user=cls.user, game=cls.game, tags=[cls.tag])

    @classmethod
    def tearDownClass(cls):
        cls.listing.delete()
        cls.game.delete()
        cls.tag.delete()
        cls.staff_user.delete()
        cls.user.delete()

    def setUp(self):
        self.client = Client()
        self.client.logout()
        self.test_image = create_image(
            num=3242342334, user=self.user, listing=self.listing)
        self.form = CreateServerListingForm({
            'game': self.game.id,
            'tags': [self.tag.id],
            'owner': self.user.id,
            'title': "Title",
            'short_description': '',
            'long_description': '',
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok'})
        self.form.data['short_description'] = (
            'a' * self.form.fields['short_description'].min_length)
        self.form.data['long_description'] = (
            'a' * self.form.fields['long_description'].min_length)

    def test_get(self):
        '''Test GET'''
        # Guest
        response = self.client.get(reverse('server_create'))
        self.assertEqual(response.status_code, 302)
        # Registered
        self.client.force_login(self.user)
        response = self.client.get(reverse('server_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'server_create.html')

    @patch("cloudinary.uploader.upload", autospec=True)
    def test_post(self, mock_upload):
        '''Test POST'''
        self.client.force_login(self.user)
        # Create fake image
        image_file = create_image_obj()
        data = {
            'game': self.game.id,
            'tags': [self.tag.id],
            'owner': self.user.id,
            'title': "Title",
            'short_description':
                'a' * self.form.fields['short_description'].min_length,
            'long_description':
                'a' * self.form.fields['long_description'].min_length,
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok',
            'image': image_file}
        fake_upload_result = {
            'url': 'https://fake-url.com/fake-image.jpg',
            'public_id': 'fake-image-id'}
        mock_upload.return_value = fake_upload_result
        response = self.client.post(reverse(
            'server_create'), data=data, follow=True)
        # Asserts
        self.assertTrue(response.status_code == 200)
        mock_upload.assert_called()
        mock_upload.assert_called_once()
        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)


class TestServerEdit(TestCase):
    '''Tests server_edit view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(
            num=34534634)
        cls.staff_user = create_user_staff(
            num=324543)
        cls.tag = create_tag(
            num=7654565)
        cls.game = create_game(
            num=2345445)
        cls.listing = create_listing(
            num=7653456, user=cls.user, game=cls.game, tags=[cls.tag])
        cls.listing2 = create_listing(
            num=23423643, user=cls.user, game=cls.game, tags=[cls.tag])
        cls.image = create_image(
            num=323423455, user=cls.user, listing=cls.listing, status=0)

    @classmethod
    def tearDownClass(cls):
        cls.image.delete()
        cls.listing.delete()
        cls.game.delete()
        cls.tag.delete()
        cls.staff_user.delete()
        cls.user.delete()

    def test_get(self):
        '''Test request method GET'''
        # Guest
        user2 = create_user(23432523)
        response = self.client.get(reverse(
            'server_edit', args=[self.listing.id]))
        self.assertEqual(response.status_code, 302)
        # Registered non-authorised user
        self.client.force_login(user2)
        response = self.client.get(reverse(
            'server_edit', args=[self.listing.id]))
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        # Registered
        self.client.force_login(self.user)
        response = self.client.get(reverse(
            'server_edit', args=[self.listing.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'server_edit.html')

    def test_get_image_status_0(self):
        '''Test GET with image status 0'''
        listing = create_listing(
            num=67566756, user=self.user, game=self.game, tags=[self.tag])
        create_image(
            num=768678, user=self.user, listing=listing, status=0)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('server_edit', args=[listing.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_image_status_1(self):
        '''Test GET with image status 1'''
        listing = create_listing(
            num=234234556, user=self.user, game=self.game, tags=[self.tag])
        create_image(
            num=123213123, user=self.user, listing=listing, status=1)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('server_edit', args=[listing.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_image_status_2(self):
        '''Test GET with image status 3'''
        listing = create_listing(
            num=23423423, user=self.user, game=self.game, tags=[self.tag])
        create_image(
            num=2341234123, user=self.user, listing=listing, status=2)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('server_edit', args=[listing.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_image_status_3(self):
        '''Test GET with image status 3'''
        listing = create_listing(
            num=2342355642, user=self.user, game=self.game, tags=[self.tag])
        create_image(
            num=2343425, user=self.user, listing=listing, status=3)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('server_edit', args=[listing.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_image_none(self):
        '''Test GET with image as None'''
        listing = create_listing(
            num=45343454, user=self.user, game=self.game, tags=[self.tag])
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('server_edit', args=[listing.id]))
        self.assertEqual(response.status_code, 200)

    @patch("cloudinary.uploader.upload", autospec=True)
    @patch("cloudinary.uploader.destroy", autospec=True)
    def test_post_update_listing_with_image_already(self,
                                                    mock_destroy,
                                                    mock_upload):
        '''Test POST and updating a listing that already have an
        image linked to it.'''
        self.client.force_login(self.user)
        image_file = create_image_obj()
        # Fake listing data
        data = {
            'game': self.game.id,
            'tags': [self.tag.id],
            'owner': self.user.id,
            'title': "Title",
            'short_description':
                'a' * 150,
            'long_description':
                'a' * 200,
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok',
            'image': image_file}

        # Create fake results from mock upload
        fake_upload_result = {
            'success': True,
            'url': 'fakeurlcom',
            'public_id': 'FakePublicID'}
        mock_upload.return_value = fake_upload_result

        # Assert correct details are being used for form
        self.assertTrue(CreateServerListingForm(data).is_valid())
        # POST
        response = self.client.post(
            reverse('server_edit', args=[self.listing.id]), data, follow=True)

        # Asserts
        self.assertTrue(response.status_code == 200)
        mock_upload.assert_called()
        mock_upload.assert_called_once()
        mock_destroy.assert_called()
        mock_destroy.assert_called_once()

        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)

    @patch("cloudinary.uploader.upload", autospec=True)
    def test_post_update_listing_with_no_image(self, mock_upload):
        '''Test POST and updating a listing that currently does not
        have an image linked to it.'''
        self.client.force_login(self.user)
        image_file = create_image_obj()
        # Fake listing data
        data = {
            'game': self.game.id,
            'tags': [self.tag.id],
            'owner': self.user.id,
            'title': "Title",
            'short_description':
                'a' * 150,
            'long_description':
                'a' * 200,
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok',
            'image': image_file}
        # Create fake results from mock upload
        fake_upload_result = {
            'success': True,
            'url': 'http://www.fakeurl.com',
            'public_id': 'FakePublicID'}
        mock_upload.return_value = fake_upload_result
        # Assert correct details are being used for form
        self.assertTrue(CreateServerListingForm(data).is_valid())
        # POST
        response = self.client.post(
            reverse('server_edit', args=[self.listing2.id]), data, follow=True)
        # Asserts
        self.assertTrue(response.status_code == 200)
        mock_upload.assert_called()
        mock_upload.assert_called_once()
        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)

    @patch("cloudinary.uploader.destroy", autospec=True)
    def test_post_delete_listing(self, mock_destroy):
        '''Test POST delete listing, also tests server_delete()'''
        self.client.force_login(self.user)
        data = {
            'server_listing_delete_confirm': 'delete'
        }

        fake_destroy_result = {
            'success': True,
        }
        mock_destroy.return_value = fake_destroy_result
        response = self.client.post(
            reverse('server_edit', args=[self.listing.id]), data, follow=True)

        self.assertTrue(response.status_code == 200)
        mock_destroy.assert_called()
        mock_destroy.assert_called_once()
        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)


class TestMyAccount(TestCase):
    '''Tests my_account view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(
            num=34565462435)
        cls.staff_user = create_user_staff(
            num=2344363456)
        cls.tag = create_tag(
            num=5152332453453783)
        cls.game = create_game(
            num=345425534)
        cls.listing = create_listing(
            num=3452376, user=cls.user, game=cls.game, tags=[cls.tag])
        cls.image = create_image(
            num=74652323, user=cls.user, listing=cls.listing, status=0)
        cls.bump = create_bump(
            user=cls.user, listing=cls.listing)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = Client()
        self.client.logout()

    def test_get(self):
        '''Test request method GET'''
        # Guest
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 302)
        # Registered non-authorised user
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        # Registered
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/my_account.html'
        )

    def test_staff_image_review_status_text(self):
        '''Check image status text'''
        self.client.force_login(self.user)
        self.image.status = 0
        self.image.save()
        response = self.client.get(reverse('my_account'))
        self.assertContains(response, 'Awaiting review')

        self.image.status = 1
        self.image.save()
        response = self.client.get(reverse('my_account'))
        self.assertContains(response, 'Approved')

        self.image.status = 2
        self.image.save()
        response = self.client.get(reverse('my_account'))
        self.assertContains(response, 'Rejected')

        self.image.status = 3
        self.image.save()
        response = self.client.get(reverse('my_account'))
        self.assertContains(response, 'Banned')

        create_listing(
            num=34233, user=self.user, game=self.game, tags=[self.tag])
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)

    @patch("cloudinary.uploader.destroy", autospec=True)
    def test_post_delete_listing(self, mock_destroy):
        '''Test POST delete listing, also tests server_delete()'''
        self.client.force_login(self.user)
        data = {
            'server_listing_delete_confirm': 'delete',
            'itemID': self.listing.id}

        fake_destroy_result = {
            'success': True,
        }
        mock_destroy.return_value = fake_destroy_result
        response = self.client.post(
            reverse('my_account'), data, follow=True)

        self.assertTrue(response.status_code == 200)
        mock_destroy.assert_called()
        mock_destroy.assert_called_once()

        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)

    def test_post_delete_account(self):
        '''Test POST account delete'''
        self.client.force_login(self.user)
        data = {
            'account_delete_confirm': 'remove'}
        response = self.client.post(
            reverse('my_account'), data, follow=True)
        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/account_deleted/']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)


class TestSignUpView(TestCase):
    '''Tests sign_up_view view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=34534546)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get(self):
        '''Test request method GET'''
        # Guest
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/signup.html')

    @patch("website.views.send_email_verification", autospec=True)
    def test_post(self, send_mail_mock):
        '''Test post, sign up new account'''
        data = {
            'username': 'tUser_3423422',
            'email': 'gniaqhhsdmbhtwekpx@bbitf.com',
            'password1': 'testpassword34234!',
            'password2': 'testpassword34234!'
        }
        # Assert fpr Form
        self.assertTrue(SignupForm(data).is_valid())
        # POST
        response = self.client.post(reverse('signup'), data, follow=True)
        # Asserts
        send_mail_mock.assert_called()
        send_mail_mock.assert_called_once()
        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/signup_verify_email']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)

    def test_post_with_form_errors(self):
        '''Test post, sign up new account'''
        data = {
            'username': 'a' * 100,
            'email': '34232v23787f324f@34f9sdfsd02392.com',
            'password1': '1!',
            'password2': '1!'
        }
        response = self.client.post(reverse('signup'), data, follow=True)
        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = []
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)


class TestActivate(TestCase):
    '''Tests activate'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=74452345)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_activation_successful(self):
        '''Test activation process works'''
        response = self.client.get(reverse(
            'activate', args=[self.uid, self.token]))
        self.assertRedirects(response, reverse('email_address_verified'))
        # Check that the user's email_verified field is True
        self.assertTrue(CustomUser.objects.get(pk=self.user.pk).email_verified)

    def test_activation_invalid_link(self):
        '''Test activation process with invalid link'''
        response = self.client.get(reverse(
            'activate', args=['invalid_uid', 'invalid_token']))
        # Check that the response returns a HttpResponse with expected message.
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content, b"Activation link is invalid!")


class TestListingsView(TestCase):
    '''Tests listings_view view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=12342543)
        cls.tag1 = create_tag(num=342342367)
        cls.tag2 = create_tag(num=342346324)
        cls.game = create_game(num=890902322)
        cls.listing = create_listing(
            num=7837842, user=cls.user, game=cls.game,
            tags=[cls.tag1, cls.tag2])
        cls.bump = create_bump(user=cls.user, listing=cls.listing)

    @classmethod
    def tearDownClass(cls):
        cls.bump.delete()
        cls.listing.delete()
        cls.game.delete()
        cls.tag1.delete()
        cls.tag2.delete()
        cls.user.delete()

    def setUp(self):
        pass

    def test_get_as_guest(self):
        '''Test request method GET'''
        # Guest
        response = self.client.get(reverse(
            'listings', args=[self.game.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listings.html'
        )

    def test_get_add_to_tag_string(self):
        '''Test adding to tag string'''
        # Guest
        response = self.client.get(reverse(
            'listings-with-tags',
            args=[self.game.slug, f'A%25{self.tag1.slug}']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listings.html'
        )

    def test_get_remove_from_tag_string_and_not_left_empty(self):
        '''Test removing from tag string but not left empty'''
        # Guest
        response = self.client.get(reverse(
            'listings-with-tags',
            args=[self.game.slug,
                  f'R%25{self.tag2.slug}%25{self.tag1.slug}'
                  f'%25{self.tag2.slug}']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listings.html'
        )

    def test_get_remove_from_tag_string_so_left_empty(self):
        '''Test removing from tag string and left empty'''
        # Guest
        response = self.client.get(reverse(
            'listings-with-tags',
            args=[self.game.slug,
                  f'R%25{self.tag1.slug}%25{self.tag1.slug}']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listings.html'
        )


class TestListingView(TestCase):
    '''Test listing_view view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=12342543)
        cls.staffuser = create_user_staff(num=53423434)
        cls.tag1 = create_tag(num=342342367)
        cls.tag2 = create_tag(num=342346324)
        cls.game = create_game(num=890902322)
        cls.listing = create_listing(
            num=7837842, user=cls.user, game=cls.game,
            tags=[cls.tag1, cls.tag2])
        cls.bump = create_bump(user=cls.user, listing=cls.listing)

    def setUp(self):
        self.listing.status = 1

    @classmethod
    def tearDownClass(cls):
        cls.bump.delete()
        cls.listing.delete()
        cls.game.delete()
        cls.tag1.delete()
        cls.tag2.delete()
        cls.user.delete()
        cls.staffuser.delete()

    def test_get_as_guest(self):
        '''Test request method GET as guest'''
        # Guest
        response = self.client.get(reverse(
            'listing', args=[self.listing.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listing.html'
        )

    def test_get_as_listing_staff(self):
        '''Test request method GET as staff user'''
        self.client.force_login(user=self.staffuser)
        response = self.client.get(reverse(
            'listing', args=[self.listing.slug]))
        self.assertEqual(response.context['listing_owner'], self.user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listing.html'
        )

    def test_get_try_view_draft_listing_as_guest(self):
        '''Test to try and view a draft listing, when not the
        listing owner or staff user'''
        self.listing.status = 0
        self.listing.save()
        response = self.client.get(reverse(
            'listing', args=[self.listing.slug]))
        self.assertEqual(response.status_code, 404)

    def test_get_try_view_draft_listing_as_owner(self):
        '''Test to try and view a draft listing, when user is
        listing owner.'''
        req_fac = RequestFactory().get('/fake_path')
        req_fac.user = self.user
        self.listing.status = 0
        self.listing.save()
        self.assertAlmostEqual(self.listing.owner_id, req_fac.user.id)
        self.client.force_login(user=req_fac.user)
        response = self.client.get(reverse(
            'listing', args=[self.listing.slug]), request=req_fac)
        self.assertEqual(response.status_code, 200)

    def test_get_try_view_draft_listing_as_staff(self):
        '''Test to try and view a draft listing, when user is
        staff user.'''
        self.listing.status = 0
        self.listing.save()
        self.client.force_login(user=self.staffuser)
        response = self.client.get(reverse(
            'listing', args=[self.listing.slug]))
        self.assertEqual(response.status_code, 200)


class TestSendEmailVerification(TestCase):
    '''Test send_email_verification view'''

    @patch("django.core.mail.send_mail", autospec=True)
    def test_send_mail(self, send_mail_mock):
        '''Test send_mail function'''
        user = create_user(num=3432432424)
        request = RequestFactory().post(
            reverse('send_email_verification'), {'user': user})

        with patch("django.core.mail.send_mail", send_mail_mock):
            response = send_email_verification(request=request, user=user)
        # Asserts
        send_mail_mock.assert_called()
        send_mail_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)


class TestBumpServer(TestCase):
    '''Test bump_server view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=435345)
        cls.staffuser = create_user_staff(num=345345345)
        cls.tag1 = create_tag(num=78456345)
        cls.tag2 = create_tag(num=4354567568)
        cls.game = create_game(num=4357456465)
        cls.listing = create_listing(
            num=3454567, user=cls.user, game=cls.game,
            tags=[cls.tag1, cls.tag2])
        cls.url = reverse('bump_server')

    @classmethod
    def tearDownClass(cls):
        cls.listing.delete()
        cls.game.delete()
        cls.tag1.delete()
        cls.tag2.delete()
        cls.user.delete()
        cls.staffuser.delete()

    def setUp(self):
        pass

    def test_get_as_guest(self):
        '''Test request method GET as guest'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_as_staff_user(self):
        '''Test request method GET as guest'''
        self.client.force_login(user=self.staffuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_successful_bump(self):
        '''Test can bump server successfully'''
        self.client.force_login(user=self.staffuser)
        data = {'server_id': self.listing.id}
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, json.dumps({'result': 1}))

    def test_bump_same_listing_twice(self):
        '''Test to confirm user cannot bump same listing twice'''
        self.client.force_login(user=self.staffuser)
        data = {'server_id': self.listing.id}
        for i in range(2):
            response = self.client.post(
                self.url, data=data, content_type="application/json",
                follow=True)
            self.assertContains(response, json.dumps({'result': 1}))

    def test_bump_user_already_at_max_active_bumps(self):
        '''Test to confirm user cannot bump same listing twice'''
        listing_list = []
        for i in range(7):
            listing_list.append(create_listing(
                num=3423343+i, user=self.user, game=self.game,
                tags=[self.tag1, self.tag2]))
        self.client.force_login(user=self.staffuser)
        for item in listing_list:
            data = {'server_id': item.id}
            response = self.client.post(
                self.url, data=data, content_type="application/json",
                follow=True)
        self.assertContains(response, json.dumps({'result': 5}))


class TestCallServer(TestCase):
    '''Test call_server view'''

    @classmethod
    def setUpClass(cls):
        cls.url = reverse('call_server')
        cls.user = create_user(num=435345)
        cls.staffuser = create_user_staff(num=345345345)
        cls.tag1 = create_tag(num=78456345)
        cls.tag2 = create_tag(num=4354567568)
        cls.game = create_game(num=4357456465)
        cls.listing = create_listing(
            num=3454567, user=cls.user, game=cls.game,
            tags=[cls.tag1, cls.tag2])
        cls.image = create_image(
            num=2343452, user=cls.user, listing=cls.listing, status=0)

    @classmethod
    def tearDownClass(cls):
        cls.listing.delete()
        cls.game.delete()
        cls.tag1.delete()
        cls.tag2.delete()
        cls.user.delete()
        cls.staffuser.delete()

    def setUp(self):
        pass

    def test_get_as_guest(self):
        '''Test request method GET as guest'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_as_staff_user(self):
        '''Test request method GET as guest'''
        self.client.force_login(user=self.staffuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_image_approval_approve(self):
        '''Test case for image_approval_approve'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['image_approval_approve', self.image.id]}
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'text': "Approved"}))

    def test_image_approval_reject(self):
        '''Test case for image_approval_reject'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['image_approval_reject', self.image.id]}
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'text': "Rejected"}))

    def test_image_approval_ban(self):
        '''Test case for image_approval_ban'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['image_approval_ban', self.image.id]}
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'text': "Rejected and user banned"}))

    def test_get_game_details(self):
        '''Test case for get_game_details'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['get_game_details', self.game.id]}
        tags = Tag.objects.filter(game=self.game.id).order_by('name')
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'game': self.game.to_json(),
             'game_tags': serializers.serialize('json', tags)}))

    def test_get_tag_details(self):
        '''Test case for get_tag_details'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['get_tag_details', self.tag1.id]}
        tag = get_object_or_404(Tag, pk=self.tag1.id)
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'tag': tag.to_json()}))

    def test_search_users_username(self):
        '''Test case for search_users-username'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['search_users_username', 'a']}
        users = CustomUser.objects.filter(username__contains='a')[:100]
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True,  'users': serializers.serialize('json', users)}))

    def test_search_users_email(self):
        '''Test case for search_users_email'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['search_users_email', 'a']}
        users = CustomUser.objects.filter(email__contains='a')[:100]
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'users': serializers.serialize('json', users)}))

    def test_search_users_id(self):
        '''Test case for search_users_id'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['search_users_id', 1]}
        users = CustomUser.objects.filter(id__contains=int(1))[:100]
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': True, 'users': serializers.serialize('json', users)}))

    @patch("website.views.send_email_verification", autospec=True)
    def test_update_email_when_both_values_match(self, mock_verify):
        '''Test case for update_email'''
        self.client.force_login(user=self.staffuser)
        data = {'args': [
            'update_email', {'email1': 'testemail@bnswer34213.hdj34',
                             'email2': 'testemail@bnswer34213.hdj34'}]}
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        mock_verify.assert_called_once()
        self.assertContains(response, json.dumps(
            {'success': True, 'reason': ''}))

    def test_get_game_tags(self):
        '''Test case for get_game_tags'''
        self.client.force_login(user=self.staffuser)
        data = {'args': ['get_game_tags', self.game.id]}
        game = get_object_or_404(Game, id=self.game.id)
        tags = game.tags.all().order_by('name')
        all_tags_for_game = []
        for tag in tags:
            all_tags_for_game.append([tag.pk, tag.name])
        response = self.client.post(
            self.url, data=data, content_type="application/json",
            follow=True)
        self.assertContains(response, json.dumps(
            {'success': "tags", 'reason': all_tags_for_game}))


class TestUnbanUser(TestCase):
    '''Test for unban_user view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=435345)
        cls.staffuser = create_user_staff(num=345345345)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.staffuser.delete()

    def test_unban_user(self):
        '''Test unban user method'''
        # Ban user
        self.user.is_banned = True
        self.user.save()
        # Asser user is banned
        self.assertTrue(self.user.is_banned)
        # Login as staff
        self.client.force_login(user=self.staffuser)
        # Goto URL with arg, this should unban user.
        response = self.client.get(reverse('unban_user', args=[self.user.id]))
        # Refresh user
        self.user.refresh_from_db()
        # Assert user is unbanned.
        self.assertFalse(self.user.is_banned)
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    '''Test for login_view view'''

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(num=564598)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get_as_guest(self):
        '''Test GET as guest'''
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_get_as_user(self):
        '''Test GET'''
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_account'))

    @patch('website.views.authenticate')
    def test_post_successful_login(self, mock_auth):
        '''Test POST with correct credentials'''
        user = create_user(num='1211135')
        data = {'email': user.email,
                'password': user.password}
        mock_auth.return_value = user
        response = self.client.post(reverse('login'),
                                    data=data,
                                    Follow=True)
        mock_auth.assert_called_once()
        mock_auth.destroy()
        self.assertEqual(response.url, '/accounts/my_account')
        self.assertEqual(response.status_code, 302)

    @patch('website.views.authenticate')
    def test_post_fail_login_banned_user(self, mock_auth):
        '''Test POST with correct credentials'''
        user = create_user(num='867563')
        user.is_banned = True
        user.save()
        user.refresh_from_db()
        data = {'email': user.email,
                'password': user.password}
        mock_auth.return_value = user
        response = self.client.post(reverse('login'),
                                    data=data,
                                    Follow=True)
        mock_auth.assert_called_once()
        mock_auth.destroy()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'],
                         "This account is banned.")

    def test_post_unsuccessful_login(self):
        '''Test POST with incorrect credentials'''
        data = {
            'email': self.user.email,
            'password': '',
        }
        response = self.client.post(reverse('login'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'],
                         "Either user does not exist or password does not "
                         "match account.")
        self.assertTemplateUsed(response, 'registration/login.html')


class TestGameManagement(TestCase):
    '''Test for game_management view'''

    def test_get_as_guest(self):
        '''Test GET as guest, should redirect'''
        response = self.client.get(reverse('game_management'))
        self.assertEqual(response.status_code, 302)

    def test_get_as_non_staffuser(self):
        '''Test GET as non-staffuser, should redirect'''
        user = create_user(34234554)
        self.client.force_login(user=user)
        response = self.client.get(reverse('game_management'))
        self.assertEqual(response.status_code, 302)

    def test_get_as_staffuser(self):
        '''Test GET as staffuser, should load view'''
        staff_user = create_user_staff(2137653)
        self.client.force_login(user=staff_user)
        response = self.client.get(reverse('game_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_game_management.html')

    @patch('website.views.delete_game')
    def test_post_delete_game(self, mock_delete):
        '''Test POST as staffuser trying to delete game'''
        data = {'game_delete_confirm': ''}
        staff_user = create_user_staff(8465285)
        self.client.force_login(user=staff_user)
        response = self.client.post(reverse('game_management'), data=data)
        mock_delete.assert_called_once()
        mock_delete.destroy()
        self.assertEqual(response.status_code, 200)

    def test_post_update_game(self):
        '''Test POST as staffuser trying to update game'''
        game = create_game(342343)
        staff_user = create_user_staff(4353576)
        self.client.force_login(user=staff_user)
        data = {'id': game.id,
                'name': 'NEW NAME',
                'slug': game.slug,
                'tags': game.tags,
                'status': game.status}
        files = {}
        game = get_object_or_404(Game, pk=data["id"])
        self.assertTrue(GameManageForm(data=data, files=files, instance=game))
        response = self.client.post(reverse('game_management'),
                                    data=data, files=files)
        self.assertEqual(response.status_code, 200)

    @patch('website.views.add_new_game')
    def test_post_add_game(self, mock_func):
        '''Test POST as staffuser trying to add game'''
        data = {'id': ''}
        staff_user = create_user_staff(63456)
        self.client.force_login(user=staff_user)
        response = self.client.post(reverse('game_management'), data=data)
        mock_func.assert_called_once()
        mock_func.destroy()
        self.assertEqual(response.status_code, 200)


class TestDeleteGame(TestCase):
    '''Test for delete_game function'''

    @patch('website.views.uploader.destroy')
    def test_delete_game_with_image_successfully(self, mock_func):
        '''Test to delete game successfully'''
        game = create_game(454545, True)
        data = {'game_delete_confirm': 'delete',
                'itemID': game.id}
        response = delete_game(data)
        mock_func.assert_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content,
                         b"Success - Game deleted.")

    @patch('website.views.uploader.destroy')
    def test_delete_game_with_no_image_successfully(self, mock_func):
        '''Test to delete game successfully'''
        game = create_game(2342534)
        data = {'game_delete_confirm': 'delete',
                'itemID': game.id}
        response = delete_game(data)
        mock_func.assert_not_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content,
                         b"Success - Game deleted.")

    @patch('website.views.uploader.destroy')
    def test_delete_game_with_no_image_failed_phrase(self, mock_func):
        '''Test to delete game failed due to incorrect phrase'''
        game = create_game(2342534)
        data = {'game_delete_confirm': '',  # Intentionally blank
                'itemID': game.id}
        response = delete_game(data)
        mock_func.assert_not_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content,
                         b"Failed - No game deleted.")

    @patch('website.views.uploader.destroy')
    def test_delete_game_with_no_image_failed_no_id(self, mock_func):
        '''Test to delete game failed due to no id'''
        data = {'game_delete_confirm': 'delete',
                'itemID': ''}  # Intentionally blank
        response = delete_game(data)
        mock_func.assert_not_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content,
                         b"Failed - No game deleted.")


class TestNewGame(TestCase):
    '''Test for add_new_game function'''

    @patch('website.views.uploader.upload')
    def test_add_new_game_failed(self, mock_func):
        '''Test to add new game with no image successfully'''
        tag1 = create_tag(3928489)
        data = {
            'name': '',
            'slug': '',
            'tags': [tag1],
            'image': None,
            'status': 1,
        }
        form = MagicMock()
        form.data = {'url': 'FakeUrl'}
        mock_func.return_value = {
            'url': 'fakeURL',
        }
        response = add_new_game(data=data)
        mock_func.assert_not_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content,
                         b"Failed to add new game.")

    @patch('website.views.uploader.upload')
    def test_add_new_game_successfully_with_no_image(self, mock_func):
        '''Test to add new game with no image successfully'''
        tag1 = create_tag(3928489)
        data = {
            'name': 'Fake Game Name',
            'slug': 'fake-game-name',
            'tags': [tag1],
            'image': None,
            'status': 1,
        }
        mock_func.return_value = {
            'url': 'fakeURL',
        }
        response = add_new_game(data=data)
        mock_func.assert_not_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content,
                         b"New game added with no image.")

    @patch('website.views.uploader.upload')
    def test_add_new_game_successfully_with_image(self, mock_func):
        '''Test to add new game with image successfully'''
        tag1 = create_tag(3928489)
        data = {
            'name': 'Fake Game Name',
            'slug': 'fake-game-name',
            'tags': [tag1],
            'status': 1,
        }
        files = {
            'image': create_image_obj(),
        }
        mock_func.return_value = {
            'url': 'fakeURL',
        }
        response = add_new_game(data=data, files=files)
        mock_func.assert_called()
        mock_func.mock_destroy()
        self.assertEqual(response.content, b"New game added with image.")


class TestUpdateGame(TestCase):
    '''Test for update_game function'''

    def test_update_game_fail_bad_data_no_image(self):
        '''Test to update game with no image.
        FAIL due to missing data'''
        tag1 = create_tag(4532343)
        game = create_game(34223234)
        # name intentionally left blank
        data = {'name': '',
                'slug': 'fake-game-name',
                'tags': [tag1],
                'status': 1,
                'id': game.id}
        response = update_game(data=data)
        self.assertEqual(response.content, b"Failed - Game not updated.")

    @patch('website.views.uploader.upload')
    def test_update_game_success_no_image(self, mock_func):
        '''Test updating game when not updating image'''
        tag1 = create_tag(78392479)
        game = create_game(3343563)
        data = {'name': 'Fake Game Name',
                'slug': 'fake-game-name',
                'tags': [tag1],
                'status': 1,
                'image': None,
                'id': game.id}
        mock_func.return_value = {'url': 'fakeURL'}
        response = update_game(data=data, files=None)
        mock_func.assert_not_called()
        mock_func.mock_destroy()
        game.refresh_from_db()
        self.assertEqual(game.name, 'Fake Game Name')
        self.assertEqual(response.content, b"Success - Game updated.")

    @patch('website.views.uploader.upload')
    @patch('website.views.uploader.destroy')
    def test_update_game_success_replace_image(self, mock_destroy,
                                               mock_upload):
        '''Test updating game when updating image'''
        tag1 = create_tag(78392479)
        game = create_game(3343563)
        image = create_image_obj()
        game.image = 'place/holder/fake/place'
        game.save()
        data = {'name': 'Fame Game Name',
                'slug': 'fake-game-name',
                'tags': [tag1],
                'status': 1,
                'image:': image,
                'id': game.id}
        files = {'image': image}
        self.assertIsNotNone(game.image)
        self.assertTrue(GameManageForm(data=data, instance=game).is_valid())
        mock_upload.return_value = {'url': 'fakeURL'}
        response = update_game(data=data, files=files)
        mock_upload.assert_called()
        mock_destroy.assert_called()
        game.refresh_from_db()
        self.assertEqual(response.content, b"Success - Game updated.")

    @patch('website.views.uploader.upload')
    @patch('website.views.uploader.destroy')
    def test_update_game_success_add_image(self, mock_destroy, mock_upload):
        '''Test updating game when adding image
        when no image already attached.'''
        tag1 = create_tag(342328934)
        image_file = create_image_obj()
        game = create_game(5623234)
        game.save()
        data = {
            'name': 'Fame Game Name',
            'slug': 'fake-game-name',
            'tags': [tag1],
            'status': 1,
            'id': game.id}
        files = {'image': image_file}
        mock_upload.return_value = {
            'url': 'fakeURL',
        }
        response = update_game(data=data, files=files)
        mock_destroy.assert_not_called()
        mock_upload.assert_called()
        self.assertEqual(response.content, b"Success - Game updated.")


class TestTagManagement(TestCase):
    '''Test for `tag_management` view, this also tests:
     `add_new_tag`, `update_tag` and `delete_tag`.'''

    def test_get_as_guest(self):
        '''Test GET as guest, should redirect'''
        response = self.client.get(reverse('tag_management'))
        self.assertEqual(response.status_code, 302)

    def test_get_as_non_staffuser(self):
        '''Test GET as non-staffuser, should redirect'''
        user = create_user(53255754)
        self.client.force_login(user=user)
        response = self.client.get(reverse('tag_management'))
        self.assertEqual(response.status_code, 302)

    def test_get_as_staffuser(self):
        '''Test GET as staffuser, should load view'''
        staff_user = create_user_staff(234563)
        self.client.force_login(user=staff_user)
        response = self.client.get(reverse('tag_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff_tag_management.html')

    def test_post_delete_tag(self):
        '''Test delete_tag successful'''
        staff_user = create_user_staff(4353576)
        self.client.force_login(user=staff_user)
        tag = create_tag(3436534)
        _id = tag.id
        data = {'tag_delete_confirm': 'delete',
                'itemID': tag.id}
        response = self.client.post(reverse('tag_management'), data=data)
        self.assertFalse(Tag.objects.filter(id=_id).count())
        self.assertEqual(response.status_code, 200)

    def test_post_delete_tag_fail_bad_phrase(self):
        '''Test delete_tag fail, bad phrase'''
        staff_user = create_user_staff(4353576)
        self.client.force_login(user=staff_user)
        tag = create_tag(3436534)
        _id = tag.id
        data = {'tag_delete_confirm': 'de333let',
                'itemID': tag.id}
        response = self.client.post(reverse('tag_management'), data=data)
        self.assertTrue(Tag.objects.filter(id=_id).count())
        self.assertEqual(response.status_code, 200)

    def test_post_update_tag(self):
        '''Test POST as staffuser trying to update tag'''
        tag = create_tag(32423465)
        staff_user = create_user_staff(4353576)
        self.client.force_login(user=staff_user)
        data = {'id': tag.id, 'name': 'TESTNewName893940', 'slug': tag.slug}
        response = self.client.post(reverse('tag_management'), data=data)
        self.assertTrue(Tag.objects.filter(name='TESTNewName893940').count())
        self.assertEqual(response.status_code, 200)

    def test_post_update_tag_fail_duplicate(self):
        '''Test POST as staffuser trying to update tag but fail
        due to duplicate'''
        create_tag(22222333)
        tag = create_tag(32423465)
        staff_user = create_user_staff(37242784)
        self.client.force_login(user=staff_user)
        data = {'id': tag.id, 'name': '22222333', 'slug': '22222333'}
        response = self.client.post(reverse('tag_management'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_add_tag(self):
        '''Test POST as staffuser trying to add tag'''
        staff_user = create_user_staff(34523565)
        self.client.force_login(user=staff_user)
        data = {'id': '',
                'name': 'TEST New Tag',
                'slug': 'test_new_tag'}
        response = self.client.post(reverse('tag_management'), data=data)
        self.assertTrue(Tag.objects.filter(name=data['name']).count())
        self.assertEqual(response.status_code, 200)


class TestStaffManagementSearch(TestCase):
    '''Test for `staff_user_management_search view`'''

    def test_get_guest(self):
        '''Test GET as guest'''
        response = self.client.post(reverse('staff_user_management_search'))
        self.assertEqual(response.status_code, 302)

    def test_get_user(self):
        '''Test GET as user'''
        user = create_user(564356)
        self.client.force_login(user=user)
        response = self.client.post(reverse('staff_user_management_search'))
        self.assertEqual(response.status_code, 302)

    def test_get_staffuser(self):
        '''Test GET as guest'''
        user = create_user_staff(67533243)
        self.client.force_login(user=user)
        response = self.client.post(reverse('staff_user_management_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'staff/staff_user_management_search.html')


class TestStaffManagementUser(TestCase):
    '''Test for `staff_user_management_user view`'''

    @classmethod
    def setUpClass(cls):
        cls.staffuser = create_user_staff(22589495)
        cls.user = create_user(5664576)
        cls.tag = create_tag(8934378)
        cls.game = create_game(5367835)
        cls.listing1 = create_listing(3429343, cls.user, cls.game, [cls.tag])
        cls.listing2 = create_listing(324234, cls.user, cls.game, [cls.tag])
        cls.listing3 = create_listing(765453, cls.user, cls.game, [cls.tag])
        cls.listing4 = create_listing(8564325, cls.user, cls.game, [cls.tag])
        cls.listing5 = create_listing(3453654, cls.user, cls.game, [cls.tag])
        cls.image1 = create_image(34324, cls.user, cls.listing1, 0)
        cls.image2 = create_image(35243, cls.user, cls.listing2, 1)
        cls.image3 = create_image(57645, cls.user, cls.listing3, 2)
        cls.image4 = create_image(74535, cls.user, cls.listing4, 3)

    @classmethod
    def tearDownClass(cls):
        cls.image4.delete()
        cls.image3.delete()
        cls.image2.delete()
        cls.image1.delete()
        cls.listing4.delete()
        cls.listing3.delete()
        cls.listing2.delete()
        cls.listing1.delete()
        cls.game.delete()
        cls.tag.delete()
        cls.user.delete()

    def test_get_guest(self):
        '''Test GET as guest'''
        testuser = create_user(37839456)
        response = self.client.post(
            reverse('staff_user_management_user', args=[testuser.id]))
        self.assertEqual(response.status_code, 302)

    def test_get_user(self):
        '''Test GET as user'''
        testuser = create_user(37839456)
        user = create_user(35632432)
        self.client.force_login(user=user)
        response = self.client.post(
            reverse('staff_user_management_user', args=[testuser.id]))
        self.assertEqual(response.status_code, 302)

    def test_get_staffuser(self):
        '''Test GET as guest'''
        self.client.force_login(user=self.staffuser)
        response = self.client.post(
            reverse('staff_user_management_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'staff/staff_user_management_user.html')

    def test_post_update_user(self):
        '''Test POST to update user'''
        self.client.force_login(user=self.staffuser)
        data = {'user_management_save': '',
                'id': self.user.id,
                'username': "TEST43443243",
                'email': "TEST43443243@TEST43443243.com",
                'email_verified': self.user.email_verified,
                'is_staff': self.user.is_staff,
                'is_active': self.user.is_active,
                'is_banned': self.user.is_banned,
                'is_superuser': self.user.is_superuser}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[self.user.id]), data=data)
        self.assertTrue(CustomUser.objects.filter(
            username='TEST43443243').count())
        self.assertTrue(CustomUser.objects.filter(
            email='test43443243@test43443243.com').count())
        self.assertEqual(response.status_code, 302)

    def test_post_update_user_fail_duplicate(self):
        '''Test POST to update user but fail due to duplicate'''
        user = create_user(1111111)
        self.client.force_login(user=self.staffuser)
        data = {'user_management_save': '',
                'id': self.user.id,
                'username': user.username,
                'email': user.email,
                'email_verified': self.user.email_verified,
                'is_staff': self.user.is_staff,
                'is_active': self.user.is_active,
                'is_banned': self.user.is_banned,
                'is_superuser': self.user.is_superuser}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[self.user.id]), data=data)
        self.assertTrue(CustomUser.objects.filter(
            username=self.user.username).count())
        self.assertTrue(CustomUser.objects.filter(
            email=self.user.email).count())
        self.assertEqual(response.status_code, 200)

    def test_post_delete_target_user_success(self):
        '''Test POST to delete target user'''
        user = create_user(23365567)
        self.client.force_login(user=self.staffuser)
        data = {'delete_confirm': 'delete',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        self.assertFalse(CustomUser.objects.filter(
            email=user.email).count())
        self.assertEqual(response.status_code, 302)

    def test_post_delete_target_user_fail_bad_phrase(self):
        '''Test POST to delete target user due to bad phrase'''
        user = create_user(23365567)
        self.client.force_login(user=self.staffuser)
        data = {'delete_confirm': 'Apple',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        self.assertTrue(CustomUser.objects.filter(
            email=user.email).count())
        self.assertEqual(response.status_code, 200)

    def test_post_ban_target_user_success(self):
        '''Test POST to ban target user'''
        user = create_user(5445435)
        self.client.force_login(user=self.staffuser)
        data = {'ban_confirm': 'ban',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        user.refresh_from_db()
        self.assertTrue(user.is_banned)
        self.assertEqual(response.status_code, 302)

    def test_post_ban_target_user_fail_bad_phrase(self):
        '''Test POST to ban target user due to bad phrase'''
        user = create_user(3248765)
        self.client.force_login(user=self.staffuser)
        data = {'ban_confirm': 'Apple',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        user.refresh_from_db()
        self.assertFalse(user.is_banned)
        self.assertEqual(response.status_code, 200)

    def test_post_unban_target_user_success(self):
        '''Test POST to unban target user'''
        user = create_user(3246534)
        user.is_banned = True
        user.save()
        self.client.force_login(user=self.staffuser)
        data = {'unban': '',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        user.refresh_from_db()
        self.assertFalse(user.is_banned)
        self.assertEqual(response.status_code, 302)

    def test_post_delete_target_user_target_listing(self):
        '''Test POST delete target user's target listing'''
        user = create_user(4465563)
        listing = create_listing(3476634, user, self.game, [self.tag])
        l_id = listing.id
        user.is_banned = True
        user.save()
        self.client.force_login(user=self.staffuser)
        data = {'delete_listing_confirm': 'delete',
                'id': listing.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        self.assertFalse(ServerListing.objects.filter(
            id=l_id).count())
        self.assertEqual(response.status_code, 302)

    def test_post_delete_target_user_target_listing_fail_bad_phrase(self):
        '''Test POST delete target user's target listing fail
        due to bad phrase'''
        user = create_user(4465563)
        listing = create_listing(3476634, user, self.game, [self.tag])
        l_id = listing.id
        user.is_banned = True
        user.save()
        self.client.force_login(user=self.staffuser)
        data = {'delete_listing_confirm': 'apple',
                'id': listing.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        self.assertTrue(ServerListing.objects.filter(
            id=l_id).count())
        self.assertEqual(response.status_code, 200)

    @patch("website.views.send_email_verification")
    def test_post_send_verification_email_to_target(self, mock_verify):
        '''Test POST send verification email to user and flag use's
        email as unverified'''
        user = create_user(3243423)
        self.client.force_login(user=self.staffuser)
        data = {'email-verify': '',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        user.refresh_from_db()
        mock_verify.assert_called()
        mock_verify.mock_destroy()
        self.assertFalse(user.email_verified)
        self.assertEqual(response.status_code, 302)

    def test_post_promote_user_to_staff(self):
        '''Test POST promote user to staff'''
        user = create_user(4357843)
        self.assertFalse(user.is_staff)
        super_u = create_user_super(7482432)
        self.client.force_login(user=super_u)
        data = {'promote': '',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        user.refresh_from_db()
        self.assertTrue(user.is_staff)
        self.assertEqual(response.status_code, 302)

    def test_post_demote_user_from_staff(self):
        '''Test POST demote user from staff'''
        user = create_user(45325432)
        user.is_staff = True
        self.assertTrue(user.is_staff)
        super_u = create_user_super(4532643)
        self.client.force_login(user=super_u)
        data = {'demote': '',
                'id': user.id}
        response = self.client.post(reverse(
            'staff_user_management_user', args=[user.id]), data=data)
        user.refresh_from_db()
        self.assertFalse(user.is_staff)
        self.assertEqual(response.status_code, 302)


class TestUpdateEmail(TestCase):
    '''Tests `update_email` which also tests `check_email`'''

    def test_correct_email_formats(self):
        '''Test a bunch of emails in expected correct format'''
        req_fac = RequestFactory().get('/fake_path')
        req_fac.user = create_user(8374382)
        tests = []
        tests.append(['a@a.a', 'a@a.a'])
        tests.append(['josh@hotmail.com', 'josh@hotmail.com'])
        tests.append(['bob@123.tech', 'bob@123.tech'])
        tests.append(['dot.dot@dot.dot', 'dot.dot@dot.dot'])
        tests.append(['under_spy123@FAKEreality.unr',
                     'under_spy123@FAKEreality.unr'])
        for test in tests:
            res = update_email(req_fac, _list=test)
            self.assertEqual(res, {'result': True, 'reason': ''})

    def test_incorrect_email_formats(self):
        '''Test a bunch of emails in an unexpected correct format'''
        req_fac = RequestFactory().get('/fake_path')
        req_fac.user = create_user(8374382)
        tests = []
        tests.append(['@a', '@a'])
        tests.append(['reallyBadAtHotmail.com', 'reallyBadAtHotmail.com'])
        tests.append(['12345@1232', '12345@1232'])
        tests.append(['', ''])
        tests.append(['NoMatch@Here.com', 'DoesNot@Match.com'])
        for test in tests:
            res = update_email(req_fac, _list=test)
            self.assertNotEqual(res, {'result': True, 'reason': ''})

    def test_correct_email_duplicate(self):
        '''Test a bunch of emails in expected correct format'''
        req_fac = RequestFactory().get('/fake_path')
        req_fac.user = create_user(8374382)
        user2 = create_user(346564)
        req_fac.user.email = user2.email
        res = update_email(req_fac, _list=[user2.email, user2.email])
        self.assertEqual(
            res, {'reason': ['Email already taken. (Jackal)'],
                  'result': False})
