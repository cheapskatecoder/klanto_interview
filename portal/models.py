from django.db import models


class AccessToken(models.Model):
    access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.access_token

    class Meta:
        verbose_name = 'Access Token'
        verbose_name_plural = 'Access Tokens'


class PlaidWebhooksData(models.Model):
    json_dump = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{:%Y-%m-%d}".format(self.created_at)

