from django.db import models


class News(models.Model):
    """
    News model
    """
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    source = models.CharField(max_length=255)
    snippet = models.TextField()
    date_published = models.CharField(max_length=255)

    def __str__(self):
        return self.title