'''Tests for forms.py'''

from django.forms.widgets import PasswordInput
from django.test import TestCase
from .forms import (
    UserForm, ProfileForm, SignupForm, ConfirmAccountDeleteForm,
    ConfirmServerListingDeleteForm, ConfirmGameDeleteForm,
    UserUpdateEmailAddressForm, CreateServerListingForm,
    ImageForm, LoginForm, GameManageForm,
    TagsManageForm, ConfirmTagDeleteForm, DeleteConfirmForm
)
from .models import CustomUser, ServerListing, Game, Tag, Images


class TestUserForm(TestCase):
    '''UserForm test cases'''

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = UserForm({
            'id': '1',
            'username': ' TestName ',
            'email': 'test@email.com',
            'is_staff': False,
            'is_superuser': False})

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(self.form.fields['id'])
                         .__name__, 'IntegerField')
        self.assertEqual(type(self.form.fields['username'])
                         .__name__, 'CharField')
        self.assertEqual(type(self.form.fields['email'])
                         .__name__, 'EmailField')
        self.assertEqual(type(self.form.fields['email_verified'])
                         .__name__, 'BooleanField')
        self.assertEqual(type(self.form.fields['is_staff'])
                         .__name__, 'BooleanField')
        self.assertEqual(type(self.form.fields['is_active'])
                         .__name__, 'BooleanField')
        self.assertEqual(type(self.form.fields['is_banned'])
                         .__name__, 'BooleanField')
        self.assertEqual(type(self.form.fields['is_superuser'])
                         .__name__, 'BooleanField')

    def test_username_max_length(self):
        '''Test max_length of username'''
        self.form.data['username'] = (
            'a' * self.form.fields['username'].max_length)
        self.assertLessEqual(
            len(self.form.data['username']),
            self.form.fields['username'].max_length
        )
        self.form.data['username'] += 'a'
        self.assertGreater(
            len(self.form.data['username']),
            self.form.fields['username'].max_length
        )

    def test_username_strip(self):
        '''Test to check white spaces are removed'''
        user = self.form.save()
        self.assertTrue(self.form.is_valid())
        self.assertEqual(user.username, 'TestName')

    def test_username_required(self):
        '''Test username is required'''
        self.form.data['username'] = ''
        self.assertFalse(self.form.is_valid())

    def test_using_correct_model(self):
        '''Test to make sure using CustomUser model'''
        self.assertEqual(self.form.Meta.model, CustomUser)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', 'username', 'email', 'email_verified',
            'is_active', 'is_banned', 'is_staff', 'is_superuser'
        ])


class TestProfileForm(TestCase):
    '''ProfileForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ProfileForm({
            'email': '',
            'email_verified': False})

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(self.form.fields['email'])
                         .__name__, 'EmailField')
        self.assertEqual(type(self.form.fields['email_verified'])
                         .__name__, 'BooleanField')

    def test_email_is_required(self):
        '''Test email address is required'''
        self.assertFalse(self.form.is_valid())
        self.assertIn('email', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['email'][0],
            'Email is required. (Falcon)')

    def test_using_correct_model(self):
        '''Test to make sure using CustomUser model'''
        self.assertEqual(self.form.Meta.model, CustomUser)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, ['email', 'email_verified'])


class TestSignupForm(TestCase):
    '''SignupForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = SignupForm({
            'username': 'TestName',
            'email': 'test@email.com',
            'password1': "password",
            'password2': "password"})

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(self.form.fields['username'])
                         .__name__, 'CharField')
        self.assertEqual(type(self.form.fields['email'])
                         .__name__, 'EmailField')

    def test_using_correct_model(self):
        '''Test to make sure using CustomUser model'''
        self.assertEqual(self.form.Meta.model, CustomUser)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'username', 'email', 'password1', 'password2'])

    def test_username_is_required(self):
        '''Test username is required'''
        self.form.data['username'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('username', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['username'][0],
            'Username is required. (Ferret)')

    def test_username_max_length(self):
        '''Test max_length of username'''
        self.form.data['username'] = (
            'a' * self.form.fields['username'].max_length)
        self.assertLessEqual(
            len(self.form.data['username']),
            self.form.fields['username'].max_length
        )
        self.form.data['username'] += 'a'
        self.assertGreater(
            len(self.form.data['username']),
            self.form.fields['username'].max_length
        )

    def test_email_is_required(self):
        '''Test email is required'''
        self.form.data['email'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('email', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['email'][0],
            'Email is required. (Ferret)')

    def test_email_max_length(self):
        '''Test max_length of email'''
        self.form.data['email'] = (
            'a' * self.form.fields['email'].max_length)
        self.assertLessEqual(
            len(self.form.data['email']),
            self.form.fields['email'].max_length
        )
        self.form.data['email'] += 'a'
        self.assertGreater(
            len(self.form.data['email']),
            self.form.fields['email'].max_length
        )

    def test_email_field_does_not_have_autofocus_attribute(self):
        '''Test form will not autofocus to email field'''
        self.assertNotIn('autofocus', self.form.fields['email'].widget.attrs)


class TestConfirmAccountDeleteForm(TestCase):
    '''ConfirmAccountDeleteForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ConfirmAccountDeleteForm({
            'account_delete_confirm': 'TestName',
            'id': 1, })

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(self.form.fields['account_delete_confirm'])
                         .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using CustomUser model'''
        self.assertEqual(self.form.Meta.model, CustomUser)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', ])

    def test_confirm_max_length(self):
        '''Test max_length of account_delete_confirm'''
        self.form.data['account_delete_confirm'] = (
            'a' * self.form.fields['account_delete_confirm'].max_length)
        self.assertLessEqual(
            len(self.form.data['account_delete_confirm']),
            self.form.fields['account_delete_confirm'].max_length
        )
        self.form.data['account_delete_confirm'] += 'a'
        self.assertGreater(
            len(self.form.data['account_delete_confirm']),
            self.form.fields['account_delete_confirm'].max_length
        )

    def test_confirm_is_required(self):
        '''Test account_delete_confirm is required'''
        self.form.data['account_delete_confirm'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('account_delete_confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['account_delete_confirm'][0],
            ('To confirm deletion please type "<strong>remove</strong>" '
             'in the below box and then hit confirm'))


class TestConfirmServerListingDeleteForm(TestCase):
    '''ConfirmServerListingDeleteForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ConfirmServerListingDeleteForm({
            'server_listing_delete_confirm': 'TestName',
            'id': 1, })

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['server_listing_delete_confirm'])
            .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using ServerListing model'''
        self.assertEqual(self.form.Meta.model, ServerListing)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', ])

    def test_server_listing_delete_confirm_max_length(self):
        '''Test max_length of server_listing_delete_confirm'''
        self.form.data['server_listing_delete_confirm'] = (
            'a' * self.form.fields['server_listing_delete_confirm'].max_length)
        self.assertLessEqual(
            len(self.form.data['server_listing_delete_confirm']),
            self.form.fields['server_listing_delete_confirm'].max_length
        )
        self.form.data['server_listing_delete_confirm'] += 'a'
        self.assertGreater(
            len(self.form.data['server_listing_delete_confirm']),
            self.form.fields['server_listing_delete_confirm'].max_length
        )

    def test_server_listing_delete_confirm_is_required(self):
        '''Test server_listing_delete_confirm is required'''
        self.form.data['server_listing_delete_confirm'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('server_listing_delete_confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['server_listing_delete_confirm'][0],
            ('To confirm deletion please type "<strong>delete</strong>" '
             'in the below box and then hit confirm'))


class TestConfirmGameDeleteForm(TestCase):
    '''ConfirmGameDeleteForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ConfirmGameDeleteForm({
            'game_delete_confirm': 'TestName',
            'id': 1, })

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['game_delete_confirm'])
            .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using Game model'''
        self.assertEqual(self.form.Meta.model, Game)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', ])

    def test_game_delete_confirm_max_length(self):
        '''Test max_length of game_delete_confirm'''
        self.form.data['game_delete_confirm'] = (
            'a' * self.form.fields['game_delete_confirm'].max_length)
        self.assertLessEqual(
            len(self.form.data['game_delete_confirm']),
            self.form.fields['game_delete_confirm'].max_length
        )
        self.form.data['game_delete_confirm'] += 'a'
        self.assertGreater(
            len(self.form.data['game_delete_confirm']),
            self.form.fields['game_delete_confirm'].max_length
        )

    def test_game_delete_confirm_is_required(self):
        '''Test game_delete_confirm is required'''
        self.form.data['game_delete_confirm'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('game_delete_confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['game_delete_confirm'][0],
            ('To confirm deletion please type "<strong>delete</strong>" '
             'in the below box and then hit confirm'))


class TestUserUpdateEmailAddressForm(TestCase):
    '''UserUpdateEmailAddressForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = UserUpdateEmailAddressForm({
            'email': 'TestName',
            'email_confirm': 1, })

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['email'])
            .__name__, 'EmailField')
        self.assertEqual(type(
            self.form.fields['email_confirm'])
            .__name__, 'EmailField')

    def test_email_is_required(self):
        '''Test email is required'''
        self.form.data['email'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('email', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['email'][0],
            'Required')

    def test_email_confirm_is_required(self):
        '''Test email_confirm is required'''
        self.form.data['email_confirm'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('email_confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['email_confirm'][0],
            'Required')


class TestCreateServerListingForm(TestCase):
    '''CreateServerListingForm test cases'''

    @classmethod
    def setUpClass(cls):
        cls.tag = Tag.objects.create(
            name='testRoleplay',
            slug='testRoleplay',
        )
        cls.tag2 = Tag.objects.create(
            name='testAction',
            slug='testAction',
        )
        cls.game = Game.objects.create(
            name='gta6',
            slug='gta6',
            image=None,
            status=1,
        )
        # add created cls.tag to game.
        cls.game.tags.set([cls.tag])

    @classmethod
    def tearDownClass(cls):
        cls.game.delete()
        cls.tag.delete()
        cls.tag2.delete()

    def setUp(self):
        self.form = CreateServerListingForm({
            'game': self.game.id,
            'tags': [self.tag.id, self.tag2.id],
            'title': "Title",
            'short_description': '',
            'long_description': '',
            'status': 1,
            'discord': 'discord',
            'tiktok': 'tiktok'
        })
        self.form.data['short_description'] = (
            'a' * self.form.fields['short_description'].min_length
        )
        self.form.data['long_description'] = (
            'a' * self.form.fields['long_description'].min_length
        )

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['game'])
            .__name__, 'ModelChoiceField')
        self.assertEqual(type(
            self.form.fields['tags'])
            .__name__, 'ModelMultipleChoiceField')
        self.assertEqual(type(
            self.form.fields['title'])
            .__name__, 'CharField')
        self.assertEqual(type(
            self.form.fields['short_description'])
            .__name__, 'CharField')
        self.assertEqual(type(
            self.form.fields['long_description'])
            .__name__, 'CharField')
        self.assertEqual(type(
            self.form.fields['status'])
            .__name__, 'TypedChoiceField')
        self.assertEqual(type(
            self.form.fields['discord'])
            .__name__, 'CharField')
        self.assertEqual(type(
            self.form.fields['tiktok'])
            .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using Game model'''
        self.assertEqual(self.form.Meta.model, ServerListing)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'game', 'tags', 'title', 'short_description',
            'long_description', 'status', 'discord', 'logo',
            'tiktok'])

    def test_game_is_required(self):
        '''Test game is required'''
        self.form.data['game'] = None
        self.assertFalse(self.form.is_valid())
        self.assertIn('game', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['game'][0], (
                'Choose a game.'
            )
        )

    def test_tags_is_required(self):
        '''Test tags is required'''
        self.form.data['tags'] = None
        self.assertFalse(self.form.is_valid())
        self.assertIn('tags', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['tags'][0], (
                'Choose at least 1 tag.'
            )
        )

    def test_title_max_length(self):
        '''Test max_length of title'''
        self.form.data['title'] = (
            'a' * self.form.fields['title'].max_length)
        self.assertLessEqual(
            len(self.form.data['title']),
            self.form.fields['title'].max_length
        )
        self.form.data['title'] += 'a'
        self.assertGreater(
            len(self.form.data['title']),
            self.form.fields['title'].max_length
        )

    def test_title_is_required(self):
        '''Test title is required'''
        self.form.data['title'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('title', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['title'][0], (
                'Provide a server name.'
            )
        )

    def test_short_description_min_length(self):
        '''Test min_length of short_description'''
        self.form.data['short_description'] = (
            'a' * self.form.fields['short_description'].min_length)
        self.assertGreaterEqual(
            len(self.form.data['short_description']),
            self.form.fields['short_description'].min_length
        )
        self.form.data['short_description'] = (
            self.form.data['short_description'][:-1])
        self.assertLess(
            len(self.form.data['short_description']),
            self.form.fields['short_description'].min_length
        )
        self.assertEqual(
            self.form.errors['short_description'][0], (
                'Must be over 100 and below 200 characters.'
            )
        )

    def test_short_description_max_length(self):
        '''Test max_length of short_description'''
        self.form.data['short_description'] = (
            'a' * self.form.fields['short_description'].max_length)
        self.assertLessEqual(
            len(self.form.data['short_description']),
            self.form.fields['short_description'].max_length
        )
        self.form.data['short_description'] += 'a'
        self.assertGreater(
            len(self.form.data['short_description']),
            self.form.fields['short_description'].max_length
        )
        self.assertEqual(
            self.form.errors['short_description'][0], (
                'Must be over 100 and below 200 characters.'
            )
        )

    def test_short_description_is_required(self):
        '''Test short_description is required'''
        self.form.data['short_description'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('short_description', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['short_description'][0], (
                'Required.'
            )
        )

    def test_long_description_min_length(self):
        '''Test min_length of long_description'''

        self.form.data['long_description'] = (
            'a' * self.form.fields['long_description'].min_length
        )
        self.assertGreaterEqual(
            len(self.form.data['long_description']),
            self.form.fields['long_description'].min_length
        )
        self.form.data['long_description'] = (
            self.form.data['long_description'][:-1])
        self.assertLess(
            len(self.form.data['long_description']),
            self.form.fields['long_description'].min_length
        )
        self.assertEqual(
            self.form.errors['long_description'][0], (
                'Must be over 200 and below 2000 characters.'
            )
        )

    def test_long_description_max_length(self):
        '''Test max_length of long_description'''
        self.form.data['long_description'] = (
            'a' * self.form.fields['long_description'].max_length)
        self.assertLessEqual(
            len(self.form.data['long_description']),
            self.form.fields['long_description'].max_length
        )
        self.form.data['long_description'] += 'a'
        self.assertGreater(
            len(self.form.data['long_description']),
            self.form.fields['long_description'].max_length
        )
        self.assertEqual(
            self.form.errors['long_description'][0], (
                'Must be over 200 and below 2000 characters.'
            )
        )

    def test_long_description_is_required(self):
        '''Test long_description is required'''
        self.form.data['long_description'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('long_description', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['long_description'][0], (
                'Required.'
            )
        )

    def test_status_is_required(self):
        '''Test status is required'''
        self.form.data['status'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('status', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['status'][0], (
                'Required.'
            )
        )

    def test_status_choices_are_correct(self):
        '''Test choices are correct'''
        self.assertEqual(
            self.form.fields['status'].choices[0], (0, 'Draft'))
        self.assertEqual(
            self.form.fields['status'].choices[1], (1, 'Published'))

    def test_status_defaults_to_draft(self):
        '''Test initial value is correct'''
        form = CreateServerListingForm()
        self.assertEqual(form.fields['status'].initial, 0)

    def test_discord_is_required(self):
        '''Test discord is required'''
        self.form.data['discord'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('discord', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['discord'][0], (
                'Required.'
            )
        )

    def test_tiktok_is_not_required(self):
        '''Test tiktok is not required'''
        self.form.data['tiktok'] = ''
        self.assertTrue(self.form.is_valid())


class TestImageForm(TestCase):
    '''ImageForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ImageForm({
            'image': None,
        }
        )

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['image'])
            .__name__, 'ImageField')

    def test_using_correct_model(self):
        '''Test to make sure using Game model'''
        self.assertEqual(self.form.Meta.model, Images)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'image', ])

    def test_image_is_not_required(self):
        '''Test image is not required'''
        self.form.data['image'] = None
        self.assertTrue(self.form.is_valid())


class TestLoginForm(TestCase):
    '''LoginForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = LoginForm({
            'email': 'name@email.com',
            'password': 'password',
        }
        )

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['email'])
            .__name__, 'EmailField')
        self.assertEqual(type(
            self.form.fields['password'])
            .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using Game model'''
        self.assertEqual(self.form.Meta.model, CustomUser)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'email', 'password'
        ])

    def test_password_using_correct_widget(self):
        '''Test to make sure correct widget being used'''
        self.assertIsInstance(
            self.form.fields['password'].widget,
            PasswordInput
        )


class TestGameManageForm(TestCase):
    '''GameManageForm test cases'''

    @classmethod
    def setUpClass(cls):
        cls.tag = Tag.objects.create(
            name='testRoleplay',
            slug='testRoleplay',
        )
        cls.tag2 = Tag.objects.create(
            name='testAction',
            slug='testAction',
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = GameManageForm({
            'id': 1,
            'name': 'GameName',
            'slug': 'slug',
            'tags': [self.tag, self.tag2],
            'image': None,
            'status': 1,
        }
        )

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['id'])
            .__name__, 'IntegerField')
        self.assertEqual(type(
            self.form.fields['name'])
            .__name__, 'CharField')
        self.assertEqual(type(
            self.form.fields['slug'])
            .__name__, 'SlugField')
        self.assertEqual(type(
            self.form.fields['tags'])
            .__name__, 'ModelMultipleChoiceField')
        self.assertEqual(type(
            self.form.fields['image'])
            .__name__, 'CloudinaryFileField')
        self.assertEqual(type(
            self.form.fields['status'])
            .__name__, 'TypedChoiceField')

    def test_using_correct_model(self):
        '''Test to make sure using Game model'''
        self.assertEqual(self.form.Meta.model, Game)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', 'name', 'slug', 'tags', 'image', 'status'
        ]
        )

    def test_id_is_not_required(self):
        '''Test id is not required'''
        self.form.data['id'] = ''
        self.assertTrue(self.form.is_valid())

    def test_name_is_required(self):
        '''Test name is required'''
        self.form.data['name'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('name', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['name'][0], (
                'Required.'
            )
        )

    def test_name_max_length(self):
        '''Test max_length of name'''
        self.form.data['name'] = (
            'a' * self.form.fields['name'].max_length)
        self.assertLessEqual(
            len(self.form.data['name']),
            self.form.fields['name'].max_length
        )
        self.form.data['name'] += 'a'
        self.assertGreater(
            len(self.form.data['name']),
            self.form.fields['name'].max_length
        )

    def test_slug_max_length(self):
        '''Test max_length of slug'''
        self.form.data['slug'] = (
            'a' * self.form.fields['slug'].max_length)
        self.assertLessEqual(
            len(self.form.data['slug']),
            self.form.fields['slug'].max_length
        )
        self.form.data['slug'] += 'a'
        self.assertGreater(
            len(self.form.data['slug']),
            self.form.fields['slug'].max_length
        )

    def test_tags_is_required(self):
        '''Test tags is required'''
        self.form.data['tags'] = None
        self.assertFalse(self.form.is_valid())
        self.assertIn('tags', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['tags'][0], (
                'Choose at least 1 tag.'
            )
        )

    def test_image_is_not_required(self):
        '''Test image is not required'''
        self.form.data['image'] = None
        self.assertTrue(self.form.is_valid())

    def test_status_is_required(self):
        '''Test status is required'''
        self.form.data['status'] = None
        self.assertFalse(self.form.is_valid())
        self.assertIn('status', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['status'][0], (
                'Required.'
            )
        )

    def test_status_choices_are_correct(self):
        '''Test choices are correct'''
        self.assertEqual(
            self.form.fields['status'].choices[0], (0, 'Draft'))
        self.assertEqual(
            self.form.fields['status'].choices[1], (1, 'Published'))

    def test_status_defaults_to_draft(self):
        '''Test initial value is correct'''
        form = CreateServerListingForm()
        self.assertEqual(form.fields['status'].initial, 0)


class TestTagsManageForm(TestCase):
    '''TagsManageForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = TagsManageForm({
            'id': 1,
            'name': 'GameName',
            'slug': 'slug',
        }
        )

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['id'])
            .__name__, 'IntegerField')
        self.assertEqual(type(
            self.form.fields['name'])
            .__name__, 'CharField')
        self.assertEqual(type(
            self.form.fields['slug'])
            .__name__, 'SlugField')

    def test_using_correct_model(self):
        '''Test to make sure using correct model'''
        self.assertEqual(self.form.Meta.model, Tag)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', 'name', 'slug'
        ]
        )

    def test_name_is_required(self):
        '''Test name is required'''
        self.form.data['name'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('name', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['name'][0], (
                'Required. (Puma)'
            )
        )

    def test_name_max_length(self):
        '''Test max_length of name'''
        self.form.data['name'] = (
            'a' * self.form.fields['name'].max_length)
        self.assertLessEqual(
            len(self.form.data['name']),
            self.form.fields['name'].max_length
        )
        self.form.data['name'] += 'a'
        self.assertGreater(
            len(self.form.data['name']),
            self.form.fields['name'].max_length
        )

    def test_slug_max_length(self):
        '''Test max_length of slug'''
        self.form.data['slug'] = (
            'a' * self.form.fields['slug'].max_length)
        self.assertLessEqual(
            len(self.form.data['slug']),
            self.form.fields['slug'].max_length
        )
        self.form.data['slug'] += 'a'
        self.assertGreater(
            len(self.form.data['slug']),
            self.form.fields['slug'].max_length
        )


class TestConfirmTagDeleteForm(TestCase):
    '''ConfirmTagDeleteForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ConfirmTagDeleteForm({
            'tag_delete_confirm': 'aaaaa',
        }
        )

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['tag_delete_confirm'])
            .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using correct model'''
        self.assertEqual(self.form.Meta.model, Tag)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id',
        ]
        )

    def test_tag_delete_confirm_is_required(self):
        '''Test tag_delete_confirm is required'''
        self.form.data['tag_delete_confirm'] = None
        self.assertFalse(self.form.is_valid())
        self.assertIn('tag_delete_confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['tag_delete_confirm'][0], (
                'Follow the instructions.'
            )
        )

    def test_tag_delete_confirm_max_length(self):
        '''Test max_length of tag_delete_confirm'''
        self.form.data['tag_delete_confirm'] = (
            'a' * self.form.fields['tag_delete_confirm'].max_length)
        self.assertLessEqual(
            len(self.form.data['tag_delete_confirm']),
            self.form.fields['tag_delete_confirm'].max_length
        )
        self.form.data['tag_delete_confirm'] += 'a'
        self.assertGreater(
            len(self.form.data['tag_delete_confirm']),
            self.form.fields['tag_delete_confirm'].max_length
        )


class TestDeleteConfirmForm(TestCase):
    '''DeleteConfirmForm test cases'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = DeleteConfirmForm({
            'delete_confirm': 'Abc',
        }
        )

    def check_form_valid(self):
        '''Test to check form is valid as expected'''
        self.assertTrue(self.form.is_valid())

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(
            self.form.fields['delete_confirm'])
            .__name__, 'CharField')

    def test_delete_confirm_is_required(self):
        '''Test delete_confirm is required'''
        self.form.data['delete_confirm'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('delete_confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['delete_confirm'][0], (
                'Follow the instructions.'
            )
        )

    def test_delete_confirm_max_length(self):
        '''Test max_length of delete_confirm'''
        self.form.data['delete_confirm'] = (
            'a' * self.form.fields['delete_confirm'].max_length)
        self.assertLessEqual(
            len(self.form.data['delete_confirm']),
            self.form.fields['delete_confirm'].max_length
        )
        self.form.data['delete_confirm'] += 'a'
        self.assertGreater(
            len(self.form.data['delete_confirm']),
            self.form.fields['delete_confirm'].max_length
        )
