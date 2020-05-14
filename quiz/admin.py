from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Question)
admin.site.register(models.Submission)
admin.site.register(models.Test)
admin.site.register(models.Tag)
admin.site.register(models.UserTest)
admin.site.register(models.Course)
