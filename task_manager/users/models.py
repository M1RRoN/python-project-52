from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=255 )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
