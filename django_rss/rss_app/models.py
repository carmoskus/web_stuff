from django.db import models

# Create your models here.
class Source(models.Model):
    url = models.URLField(max_length=200, unique=True)
    last_fetched = models.DateTimeField(null=True)
    last_etag = models.TextField(default="")
    title = models.TextField(max_length=200, default="")
    description = models.TextField(max_length=999, default="")
    
    def __str__(self):
        return self.url

class Item(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    guid = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField() # Switch to time to match feedparser output?
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.url + f" {self.pub_date} {len(self.author)}/{len(self.title)}/{len(self.content)}"
    