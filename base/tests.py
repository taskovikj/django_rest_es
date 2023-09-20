from django.test import LiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from .models import CustomUser, Author, Book, Category, BlogPost, UserFollowing, Comment, Vote, UserInteraction


class CustomUserModelTestCase(TestCase):
    def test_customuser_str(self):
        user = CustomUser.objects.create(username="testuser", email="test@example.com")
        self.assertEqual(str(user), user.username)


class AuthorModelTestCase(TestCase):
    def test_author_str(self):
        author = Author.objects.create(name="Test Author", birth_date="1990-01-01", bio="Test bio")
        self.assertEqual(str(author), author.name)


class BookModelTestCase(TestCase):
    def test_book_str(self):
        author = Author.objects.create(name="Test Author", birth_date="1990-01-01", bio="Test bio")
        book = Book.objects.create(
            title="Test Book",
            author=author,
            publication_date="2022-01-01",
            isbn="1234567890123",
            genre="Test Genre",
            description="Test description"
        )
        self.assertEqual(str(book), book.title)


class CategoryModelTestCase(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name="Test Category", slug="test-category")
        self.assertEqual(str(category), category.name)


class BlogPostModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_blogpost_str(self):
        post = BlogPost.objects.create(
            title="Test Post",
            content="This is a test blog post.",
            category=self.category,
            author=self.user
        )
        self.assertEqual(str(post), post.title)


class UserFollowingModelTestCase(TestCase):
    def setUp(self):
        self.follower = CustomUser.objects.create(username="follower", email="follower@example.com")
        self.following = CustomUser.objects.create(username="following", email="following@example.com")

    def test_userfollowing_unique_together(self):
        user_following = UserFollowing(follower=self.follower, following=self.following)
        user_following.save()

        # Try to create a duplicate user following relationship (should raise IntegrityError)
        with self.assertRaises(Exception):
            duplicate_user_following = UserFollowing(follower=self.follower, following=self.following)
            duplicate_user_following.save()


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.blogpost = BlogPost.objects.create(
            title="Test Post",
            content="This is a test blog post.",
            category=self.category,
            author=self.user
        )

    def test_comment_str(self):
        comment = Comment.objects.create(
            post=self.blogpost,
            user=self.user,
            body="This is a test comment."
        )
        expected_str = f"{self.user.username} - {self.blogpost.title}"
        self.assertEqual(str(comment), expected_str)


class VoteModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.blogpost = BlogPost.objects.create(
            title="Test Post",
            content="This is a test blog post.",
            category=self.category,
            author=self.user
        )

    def test_vote_choices(self):
        vote = Vote.objects.create(user=self.user, blog_post=self.blogpost, vote=Vote.UPVOTE)
        self.assertEqual(vote.vote, Vote.UPVOTE)


class UserInteractionModelTestCase(TestCase):
    def test_userinteraction_str(self):
        user_interaction = UserInteraction(user_id="testuser", visited_url="http://example.com")
        user_interaction.save()
        self.assertIsNotNone(user_interaction.timestamp)


class HostTest(LiveServerTestCase):
    def test_home_page(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/')
        assert "BlogPost" in driver.title

    # def test_login():
    #     driver = webdriver.Chrome()
    #     driver.get('http://localhost:8000/login')
    #     username_input = driver.find_element_by_name('username')
    #     password_input = driver.find_element_by_name('password')
    #     login_button = driver.find_element_by_id('login-button')
    #
    #     username_input.send_keys('your_username')
    #     password_input.send_keys('your_password')
    #     login_button.click()
    #
    #     assert 'Welcome' in driver.page_source
    #
    #     driver.quit()


