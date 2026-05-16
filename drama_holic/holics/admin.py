from django.contrib import admin
from .models import dramas, user_drama_watching_status
from .models import animes, user_anime_watching_status
from .models import mangas, user_manga_watching_status

# Register your models here.
admin.site.register(dramas)
admin.site.register(user_drama_watching_status)
admin.site.register(animes)
admin.site.register(user_anime_watching_status)
admin.site.register(mangas)
admin.site.register(user_manga_watching_status)