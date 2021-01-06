from django.db import models


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.access_token
    
    class Meta:
        verbose_name = 'Access Token'
        verbose_name_plural = 'Access Tokens'