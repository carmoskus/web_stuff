from django.db import models

# Create your models here.
class Source(models.Model):
    url = models.URLField(max_length=200, unique=True)
    
    def __str__(self):
        return self.url

class Item(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    url = models.URLField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.url
    