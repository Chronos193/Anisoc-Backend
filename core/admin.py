from django.contrib import admin
from .models import (
    TeamMember,
    Announcement,
    Tag,
    Event,
    FanArt,
    SeasonalReport,
    BlogPost,
    FanFiction,
    Chapter,
    Comment,
)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "tenure", "is_active")
    list_filter = ("is_active", "tenure")
    search_fields = ("name", "role", "institute_email")

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "priority", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("-priority", "-created_at")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_at")
    list_filter = ("date",)
    search_fields = ("title",)
    filter_horizontal = ("tags",)

@admin.register(FanArt)
class FanArtAdmin(admin.ModelAdmin):
    list_display = ("week", "artist", "artist_name", "created_at")
    search_fields = ("artist_name", "week")

@admin.register(SeasonalReport)
class SeasonalReportAdmin(admin.ModelAdmin):
    list_display = ("title", "season", "published_at")
    search_fields = ("title", "season")

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_public", "created_at")
    list_filter = ("is_public",)
    search_fields = ("title", "author__username")
    ordering = ("-created_at",)

@admin.register(FanFiction)
class FanFictionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "author__username")
    filter_horizontal = ("tags",)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "fanfiction", "chapter_number", "published_at")
    list_filter = ("fanfiction",)
    search_fields = ("title",)
    ordering = ("fanfiction", "chapter_number")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "parent_type", "parent_id", "created_at")
    list_filter = ("parent_type",)
    search_fields = ("author__username", "content")
