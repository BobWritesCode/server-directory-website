from django.test import TestCase
from .forms import (
    UserForm, ProfileForm, SignupForm, ConfirmAccountDeleteForm,
    ConfirmServerListingDeleteForm, ConfirmGameDeleteForm,
    UserUpdateEmailAddressForm, CreateServerListingForm,
    ImageForm, LoginForm, GameListForm, GameManageForm,
    TagsManageForm, ConfirmTagDeleteForm, DeleteConfirmForm
)
from .models import CustomUser, ServerListing, Game, Tag


class TestUserForm(TestCase):

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
        self.form.data['username'] = 'a' * 20
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
        self.assertEqual(self.form.Meta.fields, [
            'id', 'username', 'email', 'email_verified',
            'is_active', 'is_banned', 'is_staff', 'is_superuser'
            ])


class TestProfileForm(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.form = ProfileForm({
            'email': '',
            'email_verified': False})

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

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
        self.form.data['username'] = 'a' * 20
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
        self.form.data['email'] = 'a' * 200
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

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.form = ConfirmAccountDeleteForm({
            'confirm': 'TestName',
            'id': 1, })

    def test_correct_field_types(self):
        '''Test all field types are correct in form'''
        self.assertEqual(type(self.form.fields['confirm'])
                         .__name__, 'CharField')

    def test_using_correct_model(self):
        '''Test to make sure using CustomUser model'''
        self.assertEqual(self.form.Meta.model, CustomUser)

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Test to make sure the correct fields are to be shown'''
        self.assertEqual(self.form.Meta.fields, [
            'id', ])

    def test_confirm_max_length(self):
        '''Test max_length of confirm'''
        self.form.data['confirm'] = 'a' * 10
        self.assertLessEqual(
            len(self.form.data['confirm']),
            self.form.fields['confirm'].max_length
            )
        self.form.data['confirm'] += 'a'
        self.assertGreater(
            len(self.form.data['confirm']),
            self.form.fields['confirm'].max_length
            )

    def test_confirm_is_required(self):
        '''Test confirm is required'''
        self.form.data['confirm'] = ''
        self.assertFalse(self.form.is_valid())
        self.assertIn('confirm', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['confirm'][0],
            ('To confirm deletion please type "<strong>remove</strong>" '
             'in the below box and then hit confirm'))


class TestConfirmServerListingDeleteForm(TestCase):

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
        self.form.data['server_listing_delete_confirm'] = 'a' * 10
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
        self.form.data['game_delete_confirm'] = 'a' * 10
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
        self.form.data['title'] = 'a' * 50
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
        self.form.data['short_description'] = 'a' * 100
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
        self.form.data['short_description'] = 'a' * 200
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
        self.form.data['long_description'] = 'a' * 200
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
        self.form.data['long_description'] = 'a' * 2000
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
        print(self.form.errors)
        self.assertTrue(self.form.is_valid())