from django.db import models

class polls(models.Model):
    Pname = models.CharField(max_length=20, unique=True)
    choice = models.Choices(value=1,names=models.CharField)

    def __str__(self):
        return self.name
    

class choice(models.Model):
    Cname = models.CharField(max_length=20, unique=True)
    count = models.IntegerField()

