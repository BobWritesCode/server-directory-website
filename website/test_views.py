'''Tests for views.py'''

from unittest.mock import patch
from io import BytesIO
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import Client

from .models import CustomUser, Tag, Game, ServerListing, Images
from .forms import CreateServerListingForm


def create_user(num: int):
    '''Create test user'''
    return CustomUser.objects.create(
        username=f'T_User_{num}',
        password=f'TPass_{num}',
        email=f't_user_{num}@d8sf87sdf978sd.com',
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

def create_tag(num: int):
    '''Create test tag'''
    return Tag.objects.create(name=f'{num}', slug=f'{num}')

def create_game(num: int):
    '''Create test game'''
    return Game.objects.create(
        name=f'{num}',
        slug=f'{num}',
        image=None,
        status=1)

def create_server_listing(num: int):
    '''Create test listing'''
    obj = ServerListing.objects.create(
        game= Game.objects.all().first(),
        owner= CustomUser.objects.all().first(),
        title= f'{num}',
        short_description= 'a' * 200,
        long_description= 'a' * 200,
        status= 1,
        discord= f'{num}',
        tiktok= f'{num}')
    obj.tags.set([Tag.objects.all().first()])
    obj.save()
    return obj

class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = create_user(789234789)
        cls.staff_user = create_user_staff(72834789)
        cls.tag = create_tag(32478309)
        cls.game = create_game(23748924)
        cls.game.tags.set([cls.tag])
        cls.server_listing = create_server_listing(21673342)

    @classmethod
    def tearDownClass(cls):
        cls.server_listing.delete()
        cls.user.delete()
        cls.staff_user.delete()
        cls.game.delete()
        cls.tag.delete()

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

    def test_e404(self):
        '''Test to check getting correct page'''
        response = self.client.get(reverse('404'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            '404.html'
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
        cls.user = create_user(238904)
        cls.staff_user = create_user_staff(7548392)
        cls.tag = create_tag(890234890)
        cls.game = create_game(16473245)
        # add created cls.tag to game.
        cls.game.tags.set([cls.tag])
        cls.server_listing = ServerListing.objects.create(
            game=cls.game,
            owner=cls.user,
            status=1,
            )

    @classmethod
    def tearDownClass(cls):
        cls.server_listing.delete()
        cls.user.delete()
        cls.staff_user.delete()
        cls.game.delete()
        cls.tag.delete()

    def setUp(self):
        self.test_image = Images.objects.create(
            user=self.user,
            listing=self.server_listing,
            status=1,
        )
        self.client.logout()

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
            'staff/staff_image_review.html'
        )

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
        cls.user = create_user(98034253)
        cls.staff_user = create_user_staff(65742383)
        cls.tag = create_tag(51523783)
        cls.game = create_game(8940322)
        # add created cls.tag to game.
        cls.game.tags.set([cls.tag])
        cls.server_listing = create_server_listing(2364788)

    @classmethod
    def tearDownClass(cls):
        cls.server_listing.delete()
        cls.user.delete()
        cls.staff_user.delete()
        cls.game.delete()
        cls.tag.delete()

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.client.logout()
        self.test_image = Images.objects.create(
            user=self.user,
            listing=self.server_listing,
            status=1,
        )
        self.form = CreateServerListingForm({
            'game': self.game.id,
            'tags': [self.tag.id],
            'owner': self.user.id,
            'title': "Title",
            'short_description': '',
            'long_description': '',
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok',
            }
        )
        self.form.data['short_description'] = (
            'a' * self.form.fields['short_description'].min_length
            )
        self.form.data['long_description'] = (
            'a' * self.form.fields['long_description'].min_length
            )
        self.factory = RequestFactory()

    def tearDown(self):
        self.test_image.delete()

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
            'server_create.html'
        )

    @patch("cloudinary.uploader.upload", autospec=True)
    def test_post(self, upload_mock):
        '''Test POST'''
        self.client.force_login(self.user)

        image_data = BytesIO(b'')
        image_file = InMemoryUploadedFile(
                file=image_data,
                field_name='image',
                name='image.jpg',
                content_type='image/jpeg',
                size=image_data.getbuffer().nbytes,
                charset=None
            )

        data = {
            'game': self.game.id,
            'tags': [self.tag.id],
            'owner': self.user.id,
            'title': "Title",
            'short_description': 'a' * self.form.fields['short_description'].min_length,
            'long_description': 'a' * self.form.fields['long_description'].min_length,
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok',
            'image': image_file
            }

        fake_upload_result = {
            'url': 'https://fake-url.com/fake-image.jpg',
            'public_id': 'fake-image-id'
        }
        upload_mock.return_value = fake_upload_result

        response = self.client.post(reverse('server_create'), data=data, follow=True)
        self.assertTrue(response.status_code == 200)

        upload_mock.assert_called()
        upload_mock.assert_called_once()
