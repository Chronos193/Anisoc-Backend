from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    tenure = models.CharField(max_length=9)  # e.g. 2024-25
    image_url = models.URLField(blank=True, null=True)
    institute_email = models.EmailField(unique=True, blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    poster_url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FanArt(models.Model):
    image_url = models.URLField()
    artist_name = models.CharField(max_length=100, blank=True)
    artist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    caption = models.TextField(blank=True)
    week = models.CharField(max_length=50)  # e.g. Week 3 / Spring 2025
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.week

class SeasonalReport(models.Model):
    title = models.CharField(max_length=200)
    season = models.CharField(max_length=50)  # Winter 2025
    description = models.TextField()
    poster_url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FanFiction(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    front_page_url = models.URLField(max_length=700, blank=True, null=True)
    title = models.CharField(max_length=700)
    summary = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    fanfiction = models.ForeignKey(
        FanFiction,
        related_name="chapters",
        on_delete=models.CASCADE
    )
    chapter_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("fanfiction", "chapter_number")

    def __str__(self):
        return f"{self.fanfiction.title} - Chapter {self.chapter_number}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent_type = models.CharField(max_length=50)  # blog / fanfiction / chapter
    parent_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"
