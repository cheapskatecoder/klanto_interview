from django.contrib import admin
from portal.models import AccessToken, PlaidWebhooksData


class AccessTokenModelAdmin(admin.ModelAdmin):
    fields = ['access_token']


admin.site.register(AccessToken, AccessTokenModelAdmin)
admin.site.register(PlaidWebhooksData)
