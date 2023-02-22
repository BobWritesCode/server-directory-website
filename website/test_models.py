'''Tests for website.models '''
import unittest
from django.core.exceptions import ValidationError
from .models import CustomUser, Tag, Game, ServerListing


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
            'email: test_user_323423234@email.com - '
            'username: TEST_user_323423234'
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
        self.assertIn('No spaces allowed. (Anaconda)', err.exception.messages)


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


class TestGame(unittest.TestCase):
    '''Tests for Game model'''

    @classmethod
    def setUpClass(cls):
        cls.tag1 = Tag.objects.create(
            name='TEST tag 323423234',
            slug='test-tag-323423234',
        )
        cls.tag2 = Tag.objects.create(
            name='test tag 213124523',
            slug='test-tag-213124523',
        )
        cls.tag3 = Tag.objects.create(
            name='teST tag 432412342',
            slug='test-tag-432412342',
        )

    @classmethod
    def tearDownClass(cls):
        cls.tag1.delete()
        cls.tag2.delete()
        cls.tag3.delete()

    def setUp(self):
        self.game1 = Game.objects.create(
            name='TEST game 323423234',
            slug='test-game-323423234',
        )
        self.game1.tags.set([self.tag1])
        self.game2 = Game.objects.create(
            name='test game 213124523',
            slug='test-game-213124523',
        )
        self.game2.tags.set([self.tag1])
        self.game3 = Game.objects.create(
            name='teST game 432412342',
            slug='test-game-432412342',
        )
        self.game3.tags.set([self.tag1])

    def tearDown(self):
        self.game1.delete()
        self.game2.delete()
        self.game3.delete()

    def test_class_string(self):
        '''Testing __str__ gives expected output'''
        expected_output = f"{self.game1}"
        self.assertEqual(str(self.game1), expected_output)

    def test_json_dump_is_as_expected(self):
        '''Test JSON convert obj to str as expected'''
        json = self.game1.to_json()
        self.assertEqual(type(json), str)
        self.assertIn('id', json)
        self.assertIn(str(self.game1.id), json)
        self.assertIn('name', json)
        self.assertIn(str(self.game1.name), json)
        self.assertIn('slug', json)
        self.assertIn(str(self.game1.slug), json)
        self.assertIn('status', json)
        self.assertIn(str(self.game1.status), json)


class TestServerListing(unittest.TestCase):
    '''Tests for ServerListing model'''

    @classmethod
    def setUpClass(cls):
        cls.tag1 = Tag.objects.create(
            name='TEST tag 323423234',
            slug='test-tag-323423234',
        )
        cls.tag2 = Tag.objects.create(
            name='TEST tag 213343243',
            slug='test-tag-213343243',
        )
        cls.game1 = Game.objects.create(
            name='TEST game 323423234',
            slug='test-game-323423234',
        )
        cls.game1.tags.set([cls.tag1])
        cls.user1 = CustomUser.objects.create(
            username='TEST_user_323423234',
            email='test_user_323423234@email.com',
        )

    @classmethod
    def tearDownClass(cls):
        cls.game1.delete()
        cls.tag1.delete()

    def setUp(self):
        self.listing1 = ServerListing.objects.create(
            game=self.game1,
            owner=self.user1,
            title="TEST LISTING 3242363",
            slug='test-listing-3242363',
            short_description='a' * ServerListing._meta.get_field(
                'short_description').max_length,
            long_description='a' * ServerListing._meta.get_field(
                'long_description').max_length,
            discord="discord",
        )
        self.listing1.tags.set([self.tag1, self.tag2])

    def tearDown(self):
        self.listing1.delete()

    def test_class_string(self):
        '''Testing __str__ gives expected output'''
        expected_output = f"{self.listing1.title}"
        self.assertEqual(str(self.listing1), expected_output)

    def test_check_tag_count_on_listing(self):
        '''Checks get correct number of tags for a listing'''
        self.assertEqual(self.listing1.number_of_tags(), 2)

    def test_save_assigns_correct_slug(self):
        '''
        Test to see if next_id is assigned correctly.
        '''
        listing2 = ServerListing.objects.create(
            game=self.game1,
            owner=self.user1,
            title="TEST LISTING 7823142",
            slug='test-listing-7823142',
            short_description='a' * ServerListing._meta.get_field(
                'short_description').max_length,
            long_description='a' * ServerListing._meta.get_field(
                'long_description').max_length,
            discord="discord",
        )
        listing2.tags.set([self.tag1, self.tag2])
        self.assertEqual(listing2.slug, f'Listing-{listing2.pk}')
        listing2.save()
        self.assertEqual(listing2.slug, f'Listing-{listing2.pk}')
