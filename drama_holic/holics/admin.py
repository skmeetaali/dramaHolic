from django.contrib import admin
from .models import drama, user_watching_status
# Register your models here.
admin.site.register(drama)
admin.site.register(user_watching_status)