from django.test import TestCase
from .models import Poll,Choice
from django.urls import reverse

        
class PollModelTest(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(name="test poll")
        self.choice = Choice.objects.create(poll=self.poll, name="1")

    def test_poll_creation(self):
        poll = Poll.objects.get(name="test poll")
        self.assertEqual(poll.name, "test poll")

    def test_choice_creation(self):
        choice = Choice.objects.get(name="1")
        self.assertEqual(choice.name, "1")
        self.assertEqual(choice.poll.name, "test poll")

    def test_vote_count(self):
        self.assertEqual(self.choice.vote_count, 0)
        self.choice.vote_count += 1
        self.choice.save()
        self.assertEqual(self.choice.vote_count, 1)


class PollViewTest(TestCase):
    def setUp(self):
        Poll.objects.create(name="test poll")

    def test_poll_list(self):
        response = self.client.get(reverse('mypoll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test poll")