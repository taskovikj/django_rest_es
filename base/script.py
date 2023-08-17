import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from django.utils.text import slugify
from random import choice, randint
from faker import Faker
from your_app.models import CustomUser, Category, BlogPost
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()

def create_random_categories(num_categories):
    for _ in range(num_categories):
        name = fake.word()
        slug = slugify(name)
        Category.objects.create(name=name, slug=slug)

def create_random_users(num_users):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = 'Branislav223!'
        user = User.objects.create_user(username=username, email=email, password=password)

def create_random_blog_posts(num_posts):
    users = User.objects.all()
    categories = Category.objects.all()
    for _ in range(num_posts):
        title = fake.sentence()
        content = fake.paragraphs(randint(3, 6), True)
        category = choice(categories)
        author = choice(users)
        BlogPost.objects.create(title=title, content=content, category=category, author=author)

def main():
    num_categories = 5
    num_users = 2
    num_blog_posts = 20

    create_random_categories(num_categories)
    create_random_users(num_users)
    create_random_blog_posts(num_blog_posts)

if __name__ == '__main__':
    main()
