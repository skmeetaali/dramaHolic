import uuid

from django.db import models

# Create your models here.
class drama(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512)
    total_ep = models.IntegerField()
    thumbnail_img = models.URLField(null=True)
 
    def __str__(self):
        return f"{self.id} :  {self.title}"
    
    
# class / model for storing watching status of  adrama
class user_watching_status(models.Model):
    drama = models.ForeignKey(drama, on_delete=models.CASCADE, related_name="watchstat")    # this acually means we are referencing the primary key of drama table
    last_watched_ep =models.IntegerField()
    last_released_ep = models.IntegerField(null=True, blank=True)
    watch_status = models.CharField(max_length=32,null=True, blank=True)
    last_watched_ep_info = models.CharField(max_length=1024,null=True, blank=True)
    next_ep_release_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=4096,null=True,  blank=True)


    def __str__(self):
        return f"{self.drama} : {self.last_watched_ep} : {self.last_released_ep}"

