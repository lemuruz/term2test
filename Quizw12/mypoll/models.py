from django.db import models

class Poll(models.Model):
    name = models.CharField(max_length=20, unique=True)
    private = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    name = models.CharField(max_length=50) 
    vote_count = models.IntegerField(default=0) 

    def __str__(self):
        return f"Q : {self.poll.name} - A : {self.name} ({self.vote_count} votes)"
