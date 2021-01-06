from django.contrib import admin
from portal.models import AccessToken


class AccessTokenModelAdmin(admin.ModelAdmin):
    fields = ['access_token']


admin.site.register(AccessToken, AccessTokenModelAdmin)