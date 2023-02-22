from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Tag, Game, ServerListing


class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = CustomUser.objects.create(
            username='Test_User',
            password='TestPass',
            email='test_user@email34232343.com',
            email_verified=True,
            is_active=True,
            is_staff=False,
        )
        cls.staff_user = CustomUser.objects.create(
            username='Test_Staff_User',
            password='TestPass',
            email='test_staff_user@email34232343.com',
            email_verified=True,
            is_active=True,
            is_staff=True,
        )
        cls.tag = Tag.objects.create(
            name='Roleplay',
            slug='roleplay',
            )
        cls.game = Game.objects.create(
            name='gta5',
            slug='gta5',
            image=None,
            status=1,
            )
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

    def test_staff_image_review(self):
        '''Test to check getting correct page'''
        # Unregistered user
        self.client.logout()
        response = self.client.get(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 302)

        # Registered, non-staff user
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 302)

        # Registered, staff user.
        self.client.force_login(user=self.staff_user)
        response = self.client.get(reverse('staff_image_review'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            'staff/staff_image_review.html'
            )
