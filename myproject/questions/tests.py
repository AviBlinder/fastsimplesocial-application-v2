from django.test import TestCase
from django import forms
from django.urls import resolve, reverse
from .models import Question,Answer,AnswerByUser
import views
import views_ajax
from django.contrib.auth import get_user_model
User = get_user_model()



class QuestionTests(TestCase):
    def setUp(self):
        self.email = 'testuser@yahoo.com'
        self.password = '123'
        user = User.objects.create_user(email=self.email, password=self.password)        
        Question.objects.create(question='Django', user=user)

    # def test_board_topics_view_success_status_code(self):
    #     url = reverse('boards:board_topics', kwargs={'pk': 1})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_board_topics_view_not_found_status_code(self):
    #     url = reverse('boards:board_topics', kwargs={'pk': 99})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 404)

    # def test_board_topics_url_resolves_board_topics_view(self):
    #     view = resolve('/boards/1/')
    #     self.assertEquals(view.func.view_class, TopicListView)

    # def test_board_topics_view_contains_navigation_links(self):
    #     board_topics_url = reverse('boards:board_topics', kwargs={'pk': 1})
    #     homepage_url = reverse('home')
    #     new_topic_url = reverse('boards:new_topic', kwargs={'pk': 1})
    #     response = self.client.get(board_topics_url)
    #     self.assertContains(response, 'href="{0}"'.format(homepage_url))
    #     self.assertContains(response, 'href="{0}"'.format(new_topic_url))
