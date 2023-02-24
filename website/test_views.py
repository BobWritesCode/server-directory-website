'''Tests for views.py'''

from unittest.mock import patch
from io import BytesIO
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.test import Client
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser, Tag, Game, ServerListing, Images, Bumps
from .forms import CreateServerListingForm, ImageForm, SignupForm
from .views import check_match, email_check


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
    obj = Game.objects.create(
        name=f'{num}',
        slug=f'{num}',
        image=None,
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


def form_data_server_listing(listing: object, tags: list):
    '''Data to have valid form for CreateServerListingForm'''
    return {
        'game': listing.game,
        'owner':  listing.owner,
        'title':  listing.title,
        'tags': tags,
        'short_description': listing.short_description,
        'long_description': listing.long_description,
        'status': listing.status,
        'discord': listing.discord,
        'tiktok': listing.tiktok,
    }


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
        pass

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
        cls.user = create_user(763543345)
        cls.staff_user = create_user_staff(43252435)
        cls.tag = create_tag(23435435)
        cls.game = create_game(234235654)
        cls.listing = create_listing(
            num=654643345, user=cls.user, game=cls.game, tags=[cls.tag])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
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
        pass

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
            'short_description':
                'a' * self.form.fields['short_description'].min_length,
            'long_description':
                'a' * self.form.fields['long_description'].min_length,
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

        response = self.client.post(reverse(
            'server_create'), data=data, follow=True)
        self.assertTrue(response.status_code == 200)

        upload_mock.assert_called()
        upload_mock.assert_called_once()

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
        cls.image = create_image(
            num=323423455, user=cls.user, listing=cls.listing, status=0)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.client.logout()

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
            'server_edit.html'
        )

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
    def test_post_update_listing(self, upload_mock):
        '''Test POST and updating a listing'''
        self.client.force_login(self.user)
        data = form_data_server_listing(listing=self.listing, tags=[self.tag,])

        fake_upload_result = {
            'success': True,
        }
        upload_mock.return_value = fake_upload_result

        self.assertEqual(CreateServerListingForm(data).is_valid(), True)
        response = self.client.post(
            reverse('server_edit', args=[self.listing.id]), data, follow=True)

        self.assertTrue(response.status_code == 200)
        upload_mock.assert_called()
        upload_mock.assert_called_once()

        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)

    @patch("cloudinary.uploader.destroy", autospec=True)
    def test_post_delete_listing(self, destroy_mock):
        '''Test POST delete listing, also tests server_delete()'''
        self.client.force_login(self.user)
        data = {
            'server_listing_delete_confirm': 'delete'
        }

        fake_destroy_result = {
            'success': True,
        }
        destroy_mock.return_value = fake_destroy_result

        response = self.client.post(
            reverse('server_edit', args=[self.listing.id]), data, follow=True)

        self.assertTrue(response.status_code == 200)
        destroy_mock.assert_called()
        destroy_mock.assert_called_once()

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
        self.factory = RequestFactory()
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
    def test_post_delete_listing(self, destroy_mock):
        '''Test POST delete listing, also tests server_delete()'''
        self.client.force_login(self.user)
        data = {
            'server_listing_delete_confirm': 'delete',
            'itemID': self.listing.id}

        fake_destroy_result = {
            'success': True,
        }
        destroy_mock.return_value = fake_destroy_result

        response = self.client.post(
            reverse('my_account'), data, follow=True)

        self.assertTrue(response.status_code == 200)
        destroy_mock.assert_called()
        destroy_mock.assert_called_once()

        # Check that the redirect chain has the correct paths
        redirect_chain = response.redirect_chain
        expected_paths = ['/accounts/my_account']
        actual_paths = [redirect[0] for redirect in redirect_chain]
        self.assertEqual(actual_paths, expected_paths)

    def test_post_delete_account(self):
        '''Test POST account delete'''
        self.client.force_login(self.user)
        data = {
            'account-delete-confirm': 'delete',
            'confirm': 'remove'}

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
        pass

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.client.logout()

    def test_get(self):
        '''Test request method GET'''
        # Guest
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/signup.html')

    @patch('django.core.mail.send_mail', autospec=True)
    def test_post(self, email_mock):
        '''Test post, sign up new account'''
        data = {
            'username': 'tUser_3423422',
            'email': 'gniaqhhsdmbhtwekpx@bbitf.com',
            'password1': 'testpassword34234!',
            'password2': 'testpassword34234!'
        }

        fake_email_result = {'success': True}
        email_mock.return_value = fake_email_result

        response = self.client.post(reverse('signup'), data, follow=True)

        email_mock.assert_called()
        email_mock.assert_called_once()

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


class TestServerListings(TestCase):
    '''Tests server_listings view'''

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
            'server-list', args=[self.game.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'server-list.html'
        )

    def test_get_add_to_tag_string(self):
        '''Test adding to tag string'''
        # Guest
        response = self.client.get(reverse(
            'server-list-wth-tags',
            args=[self.game.slug, f'A%25{self.tag1.slug}']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'server-list.html'
        )

    def test_get_remove_from_tag_string_and_not_left_empty(self):
        '''Test removing from tag string but not left empty'''
        # Guest
        response = self.client.get(reverse(
            'server-list-wth-tags',
            args=[self.game.slug,
                  f'R%25{self.tag2.slug}%25{self.tag1.slug}'
                  f'%25{self.tag2.slug}']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'server-list.html'
        )

    def test_get_remove_from_tag_string_so_left_empty(self):
        '''Test removing from tag string and left empty'''
        # Guest
        response = self.client.get(reverse(
            'server-list-wth-tags',
            args=[self.game.slug,
                  f'R%25{self.tag1.slug}%25{self.tag1.slug}']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'server-list.html'
        )


class TestListingDetail(TestCase):
    '''Test listing_detail view'''

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
            'listing_detail', args=[self.listing.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listing_detail.html'
        )

    def test_get_as_listing_staff(self):
        '''Test request method GET as staff user'''
        self.client.force_login(user=self.staffuser)
        response = self.client.get(reverse(
            'listing_detail', args=[self.listing.slug]))
        self.assertEqual(response.context['listing_owner'], self.user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'listing_detail.html'
        )

