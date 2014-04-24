from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, SocialConfiguration


admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(SocialConfiguration, SingletonModelAdmin)
