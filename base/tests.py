from django.test import TestCase

from .models import Category, CustomUser


class ModelTest(TestCase):

    def setUp(self):
        self.blog = Category.objects.create(name='testing1',
                                            slug='testing1')

        self.blog1 = CustomUser.objects.create(username='testuser1', password='admin', email='testing@gmail.com',
                                               status='author', bio="bio")

    def test_category_model(self):
        d = self.blog
        self.assertTrue(isinstance(d, Category))
        self.assertEquals(str(d), 'testing1')

    def test_customUser_model(self):
        d = self.blog1
        self.assertTrue(isinstance(d, CustomUser))
        self.assertEquals(str(d), 'testuser1')
