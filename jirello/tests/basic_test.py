from unittest import TestCase
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory
from jirello.models import *
from jirello.views import new_project


class TestBasic(TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

    def test_basic_2(self):
        a = 1
        assert a == 1


# class TestBasic2(TestCase):
#     "Show setup and teardown"

#     def setUp(self):
#         self.a = 1

#     def tearDown(self):
#         del self.a

#     def test_basic1(self):
#         "Basic with setup"

#         self.assertNotEqual(self.a, 2)

#     def test_basic2(self):
#         "Basic2 with setup"
#         assert self.a != 2

#     def test_fail(self):
#         "This test should fail"
#         assert self.a == 2


# class UserTest(TestCase):

#     def test_index_view_with_no_categories(self):
#         """
#         If no questions exist, an appropriate message should be displayed.
#         """
#         client = Client()
#         client.login()
#         response = get(reverse('main'))
#         self.assertEqual(response.status_code, 200)
#

class Testcreate_project(TestCase):
    def setUp(self):
    	self.factory = RequestFactory()
        self.u1 = User.objects.create_user(
            username='testuser1', email='tu1@tu.tu', password='top_secret', pk=2
        )

    def test_tt(self):
    	request = self.factory.post('jirello.new_project')
    	request.POST = {'title': 'blabla', 'description': '123', 'users': [self.u1, ] }
        request.user = self.u1
        response = new_project(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProjectModel.objects.count(), 1)