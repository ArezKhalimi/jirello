from django.test import TestCase
from django.test import Client, RequestFactory
from jirello.models import *


class TestBasic(TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

    def test_basic_2(self):
        a = 1
        assert a == 1


class TestBasic2(TestCase):
    "Show setup and teardown"

    def setUp(self):
        self.a = 1

    def tearDown(self):
        del self.a

    def test_basic1(self):
        "Basic with setup"

        self.assertNotEqual(self.a, 2)

    def test_basic2(self):
        "Basic2 with setup"
        assert self.a != 2

    def test_fail(self):
        "This test should fail"
        assert self.a == 2


class TestCreateProject(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.u1 = User.objects.create_user(
            username='testuser1',
            email='tu1@tu.tu',
            password='top_secret',
            pk=2
        )
        self.c = Client()

    def test_client_surf(self):
        "access to project for Anon User;login in;Create new project;Try bad data input;"

        response = self.c.get('/jirello/projects/', follow=True)
        self.assertContains(response, 'login', status_code=200, html=False)
        # now login in
        self.c.login(
            username=self.u1.username,
            password='top_secret'
        )
        response = self.c.get('/jirello/projects/')
        self.assertEqual(response.status_code, 200)

        # Create a new project
        first_project_input = {
            'title': 'sad',
            'description': '123',
            'users': [self.u1.pk, ]
        }
        response = self.c.post('/jirello/new_project/',
                               data=first_project_input)
        self.assertEqual(ProjectModel.objects.count(), 1)

        # Field title error
        first_project_input.pop('title')
        response = self.c.post('/jirello/new_project/',
                               data=first_project_input)
        self.assertFormError(response, 'form', 'title',
                             'This field is required.')
        self.assertEqual(ProjectModel.objects.count(), 1)
