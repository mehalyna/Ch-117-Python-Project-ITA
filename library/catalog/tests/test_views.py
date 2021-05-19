from django.test import TestCase
from django.urls import reverse

from ..models import MongoUser, Book, Author


class HomePageTest(TestCase):
    def test_get_page(self):
        response = self.client.get('/library/home/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Popular books of the week', response.content)

    def test_context(self):
        response = self.client.get('/library/home/')
        self.assertEqual([], response.context['top_books'])


class ProfileEditViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        user = MongoUser()
        user.first_name = 'test_firstname'
        user.last_name = 'test_lastname'
        user.username = 'test_username'
        user.email = 'test_email@example.com'
        user.password = 'test1234'
        user.save()

    def setUp(self) -> None:
        self.profile_edit_url = reverse('profile_edit')

    def test_unauthorized_get_page(self):
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_unauthorized(self):
        response = self.client.get(self.profile_edit_url)
        self.assertRedirects(response, (reverse('login_redirect_page') + '?next=' + reverse('profile_edit')))

    def test_get_page(self):
        self.client.login(username='test_username', password='test1234')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit profile', response.content)


class RedirectLoginTest(TestCase):

    def setUp(self) -> None:
        self.login_redirect_page = reverse('login_redirect_page')

    def test_can_access_redirect_page(self):
        response = self.client.get(self.login_redirect_page)
        self.assertEqual(response.status_code, 200)


class SearchPageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        author = Author()
        author.name = 'author'
        author.save()

        book = Book()
        book.title = 'title'
        book.author_id = author.id
        book.year = '2000'
        book.save()

    def test_get_search_page_without_result(self):
        response = self.client.get('/library/search/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Use the search tool to find the right book', response.content)

    def test_get_search_page_with_title(self):
        book = Book.objects(title='title').first()
        response = self.client.get('/library/search/?searchbar={}'.format(book.title))
        self.assertIn(b'title', response.content)

    def test_get_search_page_with_author(self):
        author = Author.objects(name='author').first()
        response = self.client.get('/library/search/?searchbar={}/'.format(author.name))
        self.assertIn(b'author', response.content)

    def test_get_search_page_with_year(self):
        book = Book.objects(year='2000').first()
        response = self.client.get('/library/search/?searchbar={}/'.format(book.year))
        self.assertIn(b'2000', response.content)


class NewsPageTest(TestCase):
    def test_get_news_page(self):
        response = self.client.get('/library/news/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'News and information about updates', response.content)


class CollectionsPageTest(TestCase):
    def test_get_collections_page(self):
        response = self.client.get('/library/collections/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Books with over 1000 pages', response.content)


class AuthorsPageTest(TestCase):
    def test_get_authors_page(self):
        response = self.client.get('/library/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Available authors', response.content)


class LoginViewTest(TestCase):
    def setUp(self) -> None:
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'testing'
        user.email = 'test@gmail.com'
        user.password = 'test1234'
        self.user = user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_login_with_valid_data(self):
        data = {
            'username': 'testing',
            'password': 'test1234'
        }
        response = self.client.post('/library/func_login', data=data)
        self.assertIn(b'Success', response.content)

    def test_login_with_invalid_username(self):
        data = {
            'username': 'not_exist_username',
            'password': 'test1234'
        }
        response = self.client.post('/library/func_login', data=data)
        self.assertIn(b'Denied', response.content)

    def test_login_with_invalid_password(self):
        data = {
            'username': 'testing',
            'password': 'invalid_pass'
        }
        response = self.client.post('/library/func_login', data=data)
        self.assertIn(b'Denied', response.content)


class RegistrationPageTest(TestCase):
    def setUp(self) -> None:
        self.registration_url = reverse('library-registration')

    def test_get_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        data = {
            'firstname': 'John',
            'lastname': 'Wick',
            'email': 'john45654645@gmail.com',
            'login': 'john123453464',
            'password': 'user1234',
            'confirm_password': 'user1234'
        }
        response = self.client.post(self.registration_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)


class BookshelfPageTest(TestCase):

    def setUp(self):
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'test111_user'
        user.email = 'test_user111@gmail.com'
        user.password = 'test1234'
        self.user = user.save()

    def tearDown(self):
        self.user.delete()

    def test_unauthorized_get_page(self):
        response = self.client.get('/library/profile_bookshelf/')
        self.assertEqual(response.status_code, 302)

    def test_get_page(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get('/library/profile_bookshelf/')
        self.assertEqual(response.status_code, 200)

    def test_recbooks_context(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get('/library/profile_bookshelf/')
        self.assertIn(b'Recommended for you', response.content)

    def test_wishlist_context(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get('/library/profile_bookshelf/')
        self.assertIn(b'Wishlist', response.content)

    def test_recbooks(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get('/library/profile_bookshelf/')
        self.assertEqual([], response.context['rec_books'])

    def test_wishbooks(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get('/library/profile_bookshelf/')
        self.assertEqual([], response.context['wishlist_books'])

class BookDetailsPageTest(TestCase):

    def setUp(self):
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'test111_user'
        user.email = 'test_user111@gmail.com'
        user.password = 'test1234'
        self.user = user.save()

        author = Author(name='author')
        self.author = author.save()

        book = Book(title='title',author_id=author.id,year='2000')
        self.book = book.save()

    def tearDown(self):
        self.user.delete()
        self.book.delete()
        self.author.delete()

    def test_get_page(self):
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.book.title.encode(), response.content)
        self.assertIn(self.book.year.encode(), response.content)
        self.assertIn(self.book.author_id.name.encode(), response.content)

    def test_unauthorized_get_page(self):
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Add to wishlist',response.content)
        self.assertNotIn(b'Add rating',response.content)
        self.assertNotIn(b'Add comment',response.content)

    def test_authorized_get_page(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add to wishlist',response.content)
        self.assertIn(b'Add rating',response.content)
        self.assertIn(b'Add comment',response.content)

    def test_add_to_wishlist(self):
        self.client.login(username='test111_user', password='test1234')
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add to wishlist',response.content)
        self.client.post(f'/library/add_to_wishlist/{str(self.book.id)}/')
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.user.reload()
        self.assertIn(b'Delete from wishlist',response.content)
        self.assertNotIn(b'Add to wishlist',response.content)
        self.assertTrue(str(self.book.id) in self.user.wishlist)

    def test_delete_from_wishlist(self):
        self.client.login(username='test111_user', password='test1234')
        self.client.post(f'/library/add_to_wishlist/{str(self.book.id)}/')
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Add to wishlist',response.content)
        self.assertIn(b'Delete from wishlist',response.content)
        self.client.post(f'/library/delete_from_wishlist/{str(self.book.id)}/')
        response = self.client.get(f'/library/book_details/{str(self.book.id)}')
        self.user.reload()
        self.assertNotIn(b'Delete from wishlist',response.content)
        self.assertIn(b'Add to wishlist',response.content)
        self.assertFalse(str(self.book.id) in self.user.wishlist)

class ChangePasswordPageTest(TestCase):
    def setUp(self):
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'testing'
        user.email = 'test_user111@gmail.com'
        user.password = 'test1234'
        self.user = user.save()

    def tearDown(self):
        self.user.delete()

    def test_change_password_with_valid_data(self):
        self.client.login(username='testing', password='test1234')
        data = {
            'old_password': 'test1234',
            'new_password': 'test12345'
        }
        response = self.client.post(reverse('change_password'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_with_invalid_data(self):
        self.client.login(username='testing', password='test1234')
        data = {
            'old_password': 'test12',
            'new_password': 'test12345'
        }
        response = self.client.post(reverse('change_password'), data=data)
        self.assertTemplateUsed(response, 'change_password.html')


class LogoutViewTest(TestCase):
    def setUp(self):
        user = MongoUser()
        user.first_name = 'test'
        user.last_name = 'test'
        user.username = 'testing'
        user.email = 'test_user111@gmail.com'
        user.password = 'test1234'
        self.user = user.save()

    def tearDown(self):
        self.user.delete()

    def test_logout(self):
        self.client.login(username='testing', password='test1234')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
