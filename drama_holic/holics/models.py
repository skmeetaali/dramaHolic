import uuid

from django.db import models

# Create your models here.
class dramas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512, null=True, blank=True)
    total_ep = models.IntegerField(null=True, blank=True)
    thumbnail_img = models.URLField(null=True)
 
    def __str__(self):
        return f"{self.id} :  {self.title}"
    
    
# class / model for storing watching status of  adrama
class user_drama_watching_status(models.Model):
    drama = models.ForeignKey(dramas, on_delete=models.CASCADE, related_name="drama_watchstat")    # this acually means we are referencing the primary key of drama table
    season = models.IntegerField(null=True, blank=True)
    last_watched_ep =models.IntegerField()
    last_released_ep = models.IntegerField(null=True, blank=True)
    watch_status = models.CharField(max_length=32,null=True, blank=True)
    last_watched_ep_info = models.CharField(max_length=1024,null=True, blank=True)
    next_ep_release_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=4096,null=True,  blank=True)


    def __str__(self):
        return f"{self.drama} : {self.last_watched_ep} : {self.last_released_ep}"

class animes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512, null=True, blank=True)
    total_ep = models.IntegerField(null=True, blank=True)
    thumbnail_img = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=32,null=True, blank=True)

class user_anime_watching_status(models.Model):
    anime = models.ForeignKey(animes, on_delete=models.CASCADE, related_name="ani_watchstat")    # this acually means we are referencing the primary key of anime table
    season = models.IntegerField(null=True, blank=True)
    last_watched_ep =models.IntegerField()
    last_released_ep = models.IntegerField(null=True, blank=True)
    watch_status = models.CharField(max_length=32,null=True, blank=True)
    last_watched_ep_info = models.CharField(max_length=1024,null=True, blank=True)
    next_ep_release_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=4096,null=True,  blank=True)
    

class mangas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512, null=True, blank=True)
    total_ep = models.IntegerField(null=True, blank=True)
    thumbnail_img = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=32,null=True, blank=True)

class user_manga_watching_status(models.Model):
    manga = models.ForeignKey(mangas, on_delete=models.CASCADE, related_name="manga_watchstat")    # this acually means we are referencing the primary key of anime table
    season = models.IntegerField(null=True, blank=True)
    last_watched_ep =models.IntegerField()
    last_released_ep = models.IntegerField(null=True, blank=True)
    watch_status = models.CharField(max_length=32,null=True, blank=True)
    last_watched_ep_info = models.CharField(max_length=1024,null=True, blank=True)
    next_ep_release_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=4096,null=True,  blank=True)