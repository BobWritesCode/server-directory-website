'''Tests for website.models '''
import unittest
from django.core.exceptions import ValidationError
from .models import CustomUser, Tag


class TestCustomerUser(unittest.TestCase):
    '''Tests for CustomUser model'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.user1 = CustomUser.objects.create(
            username='TEST_user_323423234',
            email='test_user_323423234@email.com',
        )
        self.user2 = CustomUser.objects.create(
            username='test_USER_213124523',
            email='test_user_213124523@email.com',
        )
        self.user3 = CustomUser.objects.create(
            username='teST_USer_432412342',
            email='test_user_432412342@email.com',
        )

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()

    def test_class_string(self):
        '''Testing __str__ gives expected output'''
        expected_output = (
            f'PK: {self.user1.id} - id: {self.user1.id} - '
            f'email: test_user_323423234@email.com - username: TEST_user_323423234'
        )
        self.assertEqual(str(self.user1), expected_output)

    def test_save_checking_for_existing_users(self):
        '''
        Test checking when object is updated and saves if values already
        exist in database and an error is raised.
        '''
        # Check username
        # Change to match another setUp object.
        self.user1.username = 'test_USER_213124523'
        # Try to save object, if ValidationError pass test.
        with self.assertRaises(ValidationError):
            self.user1.save()

        # Check email
        # Change to match another setUp object.
        self.user1.email = 'test_user_432412342@email.com'
        # Try to save object, if ValidationError pass test.
        with self.assertRaises(ValidationError):
            self.user1.save()

    def test_save_checking_if_spaces_in_username(self):
        '''Test to check if username has any spaces'''
        self.user1.username = ' test_USE R_213124523 '
        with self.assertRaises(ValidationError) as err:
            self.user1.save()
        self.assertIn( 'No spaces allowed. (Anaconda)', err.exception.messages)

class TestTag(unittest.TestCase):
    '''Tests for Tag model'''

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.tag1 = Tag.objects.create(
            name='TEST tag 323423234',
            slug='test-tag-323423234',
        )
        self.tag2 = Tag.objects.create(
            name='test tag 213124523',
            slug='test-tag-213124523',
        )
        self.tag3 = Tag.objects.create(
            name='teST tag 432412342',
            slug='test-tag-432412342',
        )

    def tearDown(self):
        self.tag1.delete()
        self.tag2.delete()
        self.tag3.delete()

    def test_class_string(self):
        '''Testing __str__ gives expected output'''
        expected_output = f"{self.tag1}"
        self.assertEqual(str(self.tag1), expected_output)

    def test_json_dump_is_as_expected(self):
        '''Test JSON convert obj to str as expected'''
        json = self.tag1.to_json()
        self.assertEqual(type(json), str)
        self.assertIn('name', json)
        self.assertIn('TEST tag 323423234', json)
        self.assertIn('slug', json)
        self.assertIn('test-tag-323423234', json)


