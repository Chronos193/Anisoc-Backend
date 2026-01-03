from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserSerializer, CookieTokenObtainPairSerializer, TeamMemberSerializer, AnnouncementSerializer, TagSerializer, EventSerializer, FanArtSerializer, SeasonalReportSerializer, BlogPostSerializer, FanFictionSerializer, ChapterSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission, SAFE_METHODS
from .models import TeamMember, Announcement, Tag, Event, FanArt, SeasonalReport, BlogPost, FanFiction, Chapter, Comment
from django.db.models import Q
from .pagination import FanFictionPagination
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.filters import SearchFilter
from rest_framework.throttling import ScopedRateThrottle
from dotenv import load_dotenv
import os
load_dotenv()

SECURE = os.getenv("SECURE", "False").lower() == "true"
SAMESITE = os.getenv("SAMESITE", "Lax")
# Default permission class in global setting is IsAutheticated()

# --------------------------------------------WARNING: THIS PART OF CODE IS FOR AUTH LOGIC AND VIEWS----------------------
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    # ---> ADD THESE TWO LINES <---
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup'  # Matches the 'signup' key in settings.py

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CookieTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]

        response = Response(
            {"detail": "Login successful"},
            status=status.HTTP_200_OK
        )

        # Access token (short-lived)
        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=SECURE,  # True in production (HTTPS)
            samesite=SAMESITE,
            max_age=30 * 60,
        )

        # Refresh token (long-lived)
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=SECURE,  # True in production
            samesite=SAMESITE,
            max_age=7 * 24 * 60 * 60,
        )

        return response

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class CookieTokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "No refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)

            # SimpleJWT rotation happens here
            new_access = refresh.access_token
            new_refresh = str(refresh)  # SAME object, rotated internally

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response({"detail": "Token refreshed"})

        response.set_cookie(
            "access_token",
            str(new_access),
            httponly=True,
            secure=SECURE,
            samesite=SAMESITE,
            max_age=30 * 60,
        )

        response.set_cookie(
            "refresh_token",
            new_refresh,
            httponly=True,
            secure=SECURE,
            samesite=SAMESITE,
            max_age=7 * 24 * 60 * 60,
        )

        return response



@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass

        response = Response({"detail": "Logged out"}, status=200)
        response.delete_cookie("access_token", path="/", samesite=SAMESITE)
        response.delete_cookie("refresh_token", path="/", samesite=SAMESITE)
        return response



#------------------------------------FOR FRONTEND TO CHECK IF TOKEN IS VALID OR NOT-------------------------------------------
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "email": request.user.email,
            "name": request.user.username,
        })

# The name is confusing so let me clearly document what this does. (Don't blame me after making so many views I am out of names.)
# This view is for frontend to check from backend if the user is signed in or not. It's a protected view so if user is not signed in backend will give a 401 and frontend will know. (Cheak Protected Routes Frontend for more info)
#--------------------------------------------------------------------------------------------------------------------


# Team Member Views (Only admin can post or update or delete can be read by anyone)
class TeamMemberListCreate(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

class TeamMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminUser]


# Announcement Views(Only admin can post or update or delete can be read by anyone)
class AnnouncementListCreate(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Announcement.objects.all()
        return Announcement.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

class AnnouncementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser]

# Tags Views (Only admin can create update or delete tags, can be used by anyone)
class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]

# Event Views(Only admin can create update or delete events, it can be read by anyone) 
class EventListCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    
# FanArt Views (Only admin can create update or delete events, it can be read by anyone. Note: Serializer ensures that artist should be mentioned by admin)
class FanArtListCreate(generics.ListCreateAPIView):
    queryset = FanArt.objects.all()
    serializer_class = FanArtSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

class FanArtDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FanArt.objects.all()
    serializer_class = FanArtSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

# Seasonal Views (Only admin can create update or delete events, it can be read by anyone.)
class SeasonalReportListCreate(generics.ListCreateAPIView):
    queryset = SeasonalReport.objects.all()
    serializer_class = SeasonalReportSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

class SeasonalReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeasonalReport.objects.all()
    serializer_class = SeasonalReportSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]
    
# Blog Views (Only user who are verified can post and all users can read)
class BlogPostListCreate(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Authenticated users see public posts + their own drafts
            return BlogPost.objects.filter(
                Q(is_public=True) |
                Q(author=user)
            )
        # Anonymous users see only public posts
        return BlogPost.objects.filter(is_public=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.is_public or obj.author == request.user
        return obj.author == request.user

class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthorOrReadOnly]


# Fanfiction Views (Only user who are verified can post and all users can read)

class IsFanFictionAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class FanFictionListCreate(generics.ListCreateAPIView):
    queryset = FanFiction.objects.all().order_by("-created_at")
    serializer_class = FanFictionSerializer
    pagination_class = FanFictionPagination

    # 🔥 THIS WAS MISSING
    filter_backends = [SearchFilter]
    search_fields = [
        "title",
        "summary",
        "tags__name",
    ]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FanFictionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FanFiction.objects.all()
    serializer_class = FanFictionSerializer
    permission_classes = [IsFanFictionAuthorOrReadOnly]

# Chapter Views(Only user who are verified can post and all users can read)
class IsChapterAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read is allowed to everyone
        if request.method in SAFE_METHODS:
            return True

        # Write allowed only to the fanfiction author
        return obj.fanfiction.author == request.user

class ChapterListCreate(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        fanfic_id = self.kwargs["fanfic_id"]
        return Chapter.objects.filter(fanfiction_id=fanfic_id)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        fanfic = FanFiction.objects.get(id=self.kwargs["fanfic_id"])

        if fanfic.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Not allowed")

        last_chapter = (
            Chapter.objects
            .filter(fanfiction=fanfic)
            .order_by("-chapter_number")
            .first()
        )

        next_number = 1 if not last_chapter else last_chapter.chapter_number + 1

        serializer.save(
            fanfiction=fanfic,
            chapter_number=next_number
        )


class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsChapterAuthorOrReadOnly]



# Comments (Can be read by any but written only by authenticated users)
class IsCommentAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Anyone can read comments
        if request.method in SAFE_METHODS:
            return True
        # Only author can edit/delete
        return obj.author == request.user

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        parent_type = self.request.query_params.get("parent_type")
        parent_id = self.request.query_params.get("parent_id")

        queryset = Comment.objects.all()

        if parent_type and parent_id:
            queryset = queryset.filter(
                parent_type=parent_type,
                parent_id=parent_id
            )

        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]






