'''Tests for website.models '''
import unittest
from django.core.exceptions import ValidationError
from .models import CustomUser, Tag, Game, ServerListing, Images


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


def create_server_listing(num: int):
    '''Create test listing'''
    obj = ServerListing.objects.create(
        game=Game.objects.all().last(),
        owner=CustomUser.objects.all().last(),
        title=f'{num}',
        short_description='a' * 200,
        long_description='a' * 200,
        status=1,
        discord=f'{num}',
        tiktok=f'{num}')
    obj.tags.set([Tag.objects.all().last()])
    return obj


def create_test_image():
    '''Create test image'''
    return Images.objects.create(
        user=CustomUser.objects.all().last(),
        listing=ServerListing.objects.all().last(),
        status=1)


class TestCustomerUser(unittest.TestCase):
    '''Tests for CustomUser model'''

    def setUp(self):
        self.user1 = create_user(23434234)
        self.user2 = create_user(45345345)
        self.user3 = create_user(64536456)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()

    def test_class_string(self):
        '''Testing __str__ gives expected output'''
        expected_output = (
            f'PK: {self.user1.id} - id: {self.user1.id} - '
            f'email: {self.user1.email} - '
            f'username: {self.user1.username}'
        )
        self.assertEqual(str(self.user1), expected_output)

    def test_save_checking_for_existing_users(self):
        '''
        Test checking when object is updated and saves if values already
        exist in database and an error is raised.
        '''
        # Check username
        # Change to match another setUp object.
        self.user1.username = self.user2.username
        # Try to save object, if ValidationError pass test.
        with self.assertRaises(ValidationError):
            self.user1.save()

        # Check email
        # Change to match another setUp object.
        self.user1.email = self.user2.email
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
        self.tag1 = create_tag(2131245234)
        self.tag2 = create_tag(1256344232)
        self.tag3 = create_tag(1235344563)

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
        self.assertIn(self.tag1.name, json)
        self.assertIn('slug', json)
        self.assertIn(self.tag1.slug, json)


class TestGame(unittest.TestCase):
    '''Tests for Game model'''

    @classmethod
    def setUpClass(cls):
        cls.tag1 = create_tag(97821390)
        cls.tag2 = create_tag(1231278903)
        cls.tag3 = create_tag(5483909)

    @classmethod
    def tearDownClass(cls):
        cls.tag1.delete()
        cls.tag2.delete()
        cls.tag3.delete()

    def setUp(self):
        self.game1 = create_game(23432423)
        self.game2 = create_game(234234234)
        self.game3 = create_game(324234234)

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
        cls.tag1 = create_tag(7832478)
        cls.tag2 = create_tag(2347890321489)
        cls.tag3 = create_tag(32478234)
        cls.game1 = create_game(3423434)
        cls.user1 = create_user(323443242)

    @classmethod
    def tearDownClass(cls):
        cls.game1.delete()
        cls.tag1.delete()
        cls.tag2.delete()
        cls.tag3.delete()
        cls.user1.delete()

    def setUp(self):
        self.listing1 = create_server_listing(23423423)

    def tearDown(self):
        self.listing1.delete()

    def test_class_string(self):
        '''Testing __str__ gives expected output'''
        expected_output = f"{self.listing1.title}"
        self.assertEqual(str(self.listing1), expected_output)

    def test_check_tag_count_on_listing(self):
        '''Checks get correct number of tags for a listing'''
        self.listing1.tags.set([self.tag1, self.tag2])
        self.assertEqual(self.listing1.number_of_tags(), 2)

    def test_save_assigns_correct_slug(self):
        '''
        Test to see if next_id is assigned correctly.
        '''
        listing2 = create_server_listing(3234234234230)
        self.assertEqual(listing2.slug, f'Listing-{listing2.pk}')
        listing2.save()
        self.assertEqual(listing2.slug, f'Listing-{listing2.pk}')
