from django.db import models

# Create your models here.
class Source(models.Model):
    url = models.URLField(max_length=200)

class Fetch(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

class Item(models.Model):
    fetch = models.ForeignKey(Fetch, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    pub_time = models.DateTimeField()
    