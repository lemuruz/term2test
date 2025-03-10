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

class PollClassifyTest(TestCase):
    def setUp(self):
        self.poll1 = Poll.objects.create(name="Poll 1")
        self.poll2 = Poll.objects.create(name="Poll 2")
        self.poll3 = Poll.objects.create(name="Poll 3")
        
        Choice.objects.create(poll=self.poll1, name="Choice A", vote_count=5)
        Choice.objects.create(poll=self.poll1, name="Choice B", vote_count=3)
        
        Choice.objects.create(poll=self.poll2, name="Choice C", vote_count=20)
        Choice.objects.create(poll=self.poll2, name="Choice D", vote_count=15)
        
        Choice.objects.create(poll=self.poll3, name="Choice E", vote_count=30)
        Choice.objects.create(poll=self.poll3, name="Choice F", vote_count=40)
    
    def test_poll_classification(self):
        from mypoll.views import pollclassify
        
        polls = Poll.objects.all()
        normalPoll, warmPoll, hotPoll = pollclassify(polls)
        
        self.assertIn(self.poll1, normalPoll)
        self.assertIn(self.poll2, warmPoll)
        self.assertIn(self.poll3, hotPoll)