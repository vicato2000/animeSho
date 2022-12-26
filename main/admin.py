from django.contrib import admin

from main import models


# Register your models here.

admin.site.register(models.Anime)
admin.site.register(models.Type)
admin.site.register(models.Status)
admin.site.register(models.Studio)
admin.site.register(models.Genre)
