from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
from django.core import exceptions as django_exceptions
# ------------------------------------------ WARNING: THIS PART OF CODE IS FOR AUTH ACCESS-----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    # 1. ADD THIS METHOD
    def validate_password(self, value):
        # This runs during the "Validation" phase.
        # If it fails, DRF catches it and sends a nice error message to the user.
        try:
            validate_password(value)
        except django_exceptions.ValidationError as e:
            # Convert Django error to DRF error
            raise serializers.ValidationError(e.messages)
        return value

    # 2. CLEAN UP THE CREATE METHOD
    def create(self, validated_data):
        password = validated_data.pop("password")
        # No need to validate here anymore, it's already done!
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class CookieTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

#----------------------------------------------------------------------------------------------------------------------




class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids", [])
        event = Event.objects.create(**validated_data)
        event.tags.set(tag_ids)
        return event

class FanArtSerializer(serializers.ModelSerializer):
    artist_username = serializers.CharField(
        source="artist.username",
        read_only=True
    )

    class Meta:
        model = FanArt
        fields = "__all__"

    def validate(self, data):
        artist = data.get("artist")
        artist_name = data.get("artist_name")

        if not artist and not artist_name:
            raise serializers.ValidationError(
                "You must specify either a registered artist or an artist name."
            )

        return data


class SeasonalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalReport
        fields = "__all__"

class BlogPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True
    )

    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["author"]

class FanFictionSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = FanFiction
        fields = "__all__"
        read_only_fields = ["author"]

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids", [])
        fanfic = FanFiction.objects.create(**validated_data)
        fanfic.tags.set(tag_ids)
        return fanfic

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("tag_ids", None)

        for attr, value in validated_data.items():
            if attr == "front_page_url" and value == "":
                value = None
            setattr(instance, attr, value)

        instance.save()

        if tag_ids is not None:
            instance.tags.set(tag_ids)

        return instance



class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"
        read_only_fields = ["fanfiction", "published_at", "chapter_number"]

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author"]
