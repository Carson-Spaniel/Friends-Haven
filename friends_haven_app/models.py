from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profilePictures/', default=None, null=True, blank=True)
    description = models.TextField(max_length=200, default=None, null=True, blank=True)
    rates = models.IntegerField(default=0, null=True, blank=True)
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

    # Recipe
    ingredients = models.CharField(max_length=5000, default=None, null=True, blank=True)
    instructions = models.CharField(max_length=5000, default=None, null=True, blank=True)

    # Book
    author = models.CharField(max_length=100, default=None, null=True, blank=True)

    # TV Show
    TV_where_to_watch = models.CharField(max_length=5000, default=None, null=True, blank=True)

    # Movie
    Movie_where_to_watch = models.CharField(max_length=5000, default=None, null=True, blank=True)

    # Music
    artist = models.CharField(max_length=100, default=None, null=True, blank=True)

    community_rate = models.IntegerField(default=0)

    def time_ago(self):
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - self.timestamp.replace(tzinfo=timezone.utc)

        # Extracting hours, minutes, and seconds from the time difference
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours == 1:
            return f"{hours} hour ago"
        if hours > 1:
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