from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profilePictures/', default=None, null=True, blank=True)
    description = models.TextField(max_length=200, default=None, null=True, blank=True)
    rates = models.IntegerField(default=0, null=True, blank=True)
    idolNum = models.IntegerField(default=0, null=True, blank=True)
    fanNum = models.IntegerField(default=0, null=True, blank=True)
    idols = models.CharField(max_length=50000,default=0, null=True, blank=True)
    fans = models.CharField(max_length=50000,default=0, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username}'

class Category(models.Model):
    name = models.CharField(max_length=50, null= True)
    slug = models.SlugField(unique=True, blank=True)
    sections = models.CharField(max_length=5000, null= True, blank=True)

    def save(self, *args, **kwargs):
        # Generate the slug from the name
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
    
class Post(models.Model):
    item_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts/', default=None, null=True, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    caption = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True,)
    community_rate = models.IntegerField(default=0)

    likes = models.IntegerField(default=0, null=True, blank=True)
    likedBy = models.CharField(max_length=50000,default=0, null=True, blank=True)

    sections = models.CharField(max_length=5000, null= True, blank=True)
    answers = models.CharField(max_length=5000, null= True, blank=True)

    def getLikes(self):
        return json.loads(self.likedBy)

    def getSections(self):
        return json.loads(self.sections)
    
    def getAnswers(self):
        return json.loads(self.answers)

    def time_ago(self):
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - self.timestamp.replace(tzinfo=timezone.utc)

        weeks, days = divmod(time_difference.days, 7)
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if weeks == 1:
            return f"{weeks} week ago"
        elif weeks > 1:
            return f"{weeks} weeks ago"
        elif days == 1:
            return f"{days} day ago"
        elif days > 1:
            return f"{days} days ago"
        elif hours == 1:
            return f"{hours} hour ago"
        elif hours > 1:
            return f"{hours} hours ago"
        elif minutes == 1:
            return f"{minutes} minute ago"
        elif minutes > 1:
            return f"{minutes} minutes ago"
        elif seconds == 1:
            return f"{seconds} second ago"
        else:
            return f"{seconds} seconds ago"

    def formatted_date(self):
        # Format the timestamp to display day, month, year, hour, and minute
        formatted_date = self.timestamp.strftime("%B %d, %Y at %H:%M")

        return formatted_date

    def __str__(self):
        return f'{self.creator} posted "{self.item_name}" on {self.formatted_date()}'