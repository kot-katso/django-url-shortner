from django.db import models

# Create your models here.
class Url(models.Model):
    hash_url = models.CharField(max_length=200)
    actual_url = models.CharField(max_length=200)
    hash_code = models.CharField(max_length=20, null=True, blank=True)
    click = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hash_url
