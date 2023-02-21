from django.test import TestCase
from .forms import (
    UserForm, ProfileForm, SignupForm, ConfirmAccountDeleteForm,
    ConfirmServerListingDeleteForm, ConfirmGameDeleteForm,
    UserUpdateEmailAddressForm, CreateServerListingForm,
    ImageForm, LoginForm, GameListForm, GameManageForm,
    TagsManageForm, ConfirmTagDeleteForm, DeleteConfirmForm
)
from .models import CustomUser, ServerListing, Game


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
