from django.test import TestCase
from jirello.models import *
from django.core.urlresolvers import reverse


class ProjectTestCase(TestCase):
    def setUp(self):

        ProjectModel.objects.create(
            title='projecttest1',
            desctiption='bag ' * 10,
            users='??'
        )


#
  
'''

LiveServerTestCase - HTTP GET POST requests etc.



setUp
user=user

req на создания 
проверка в бд создана

могу редактировать

project



линкование кайндов друг к друга
'''