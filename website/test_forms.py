from django.test import TestCase
from .forms import (
    UserForm, ProfileForm, SignupForm, ConfirmAccountDeleteForm,
    ConfirmServerListingDeleteForm, ConfirmGameDeleteForm,
    UserUpdateEmailAddressForm, CreateServerListingForm,
    ImageForm, LoginForm, GameListForm, GameManageForm,
    TagsManageForm, ConfirmTagDeleteForm, DeleteConfirmForm
)


class TestUserForm(TestCase):

    def setUp(self):
        self.form = UserForm({
            'id': '1',
            'username': ' TestName ',
            'email': 'test@email.com',
            'is_staff': False,
            'is_superuser': False})

    @classmethod
    def tearDownClass(cls):
        pass

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
        self.form.data['username'] = 'a' * 21
        self.assertFalse(self.form.is_valid())

    def test_username_strip(self):
        '''Test to check white spaces are removed'''
        user = self.form.save()
        self.assertTrue(self.form.is_valid())
        self.assertEqual(user.username, 'TestName')

    def test_username_required(self):
        '''Test username is required'''
        self.form.data['username'] = ''
        self.assertFalse(self.form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = UserForm()
        self.assertEqual(form.Meta.fields, [
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

    def test_email_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn('email', self.form.errors.keys())
        self.assertEqual(
            self.form.errors['email'][0],
            'Email is required. (Falcon)')

    def test_email_verified_required(self):
        self.assertFalse(self.form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = ProfileForm()
        self.assertEqual(form.Meta.fields, ['email', 'email_verified'])
        self.assertNotEquals(form.Meta.fields, ['email_verified'])
        self.assertNotEquals(form.Meta.fields, ['email'])
