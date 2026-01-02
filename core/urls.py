from django.urls import path, reverse_lazy
from .views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    CreateUserView,
    TeamMemberListCreate,
    TeamMemberDetail,
    AnnouncementListCreate,
    AnnouncementDetail,
    TagListCreate,
    TagDetail,
    EventListCreate,
    EventDetail,
    FanArtListCreate,
    FanArtDetail,
    SeasonalReportListCreate,
    SeasonalReportDetail,
    BlogPostListCreate,
    BlogPostDetail,
    FanFictionListCreate,
    FanFictionDetail,
    ChapterListCreate,
    ChapterDetail,
    CommentListCreate,
    CommentDetail,
    MeView
)
from django.contrib.auth import views as auth_views


app_name = "core"

urlpatterns = [
#-------------------------------------------------WARNING: THIS IS AUTH URLS-----------------------------------------
    path(
        "auth/register/",
        CreateUserView.as_view(),
        name="register"
    ),
    path(
        "auth/login/",
        CookieTokenObtainPairView.as_view(),
        name="login"
    ),
    path("auth/refresh/",
        CookieTokenRefreshView.as_view(), 
        name="refresh"
    ),
    path("auth/logout/",
        LogoutView.as_view(),
        name="logout"
    ),

#----------------------------------------------------------------------------------------------------------
    path("auth/me/", MeView.as_view(), name="me"),


#-----------------------------------------------For Password Reset------------------------------------------------------------------

    path(
        "auth/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name = "core/registration/password_reset.html",
            email_template_name="core/registration/password_reset_email.html",
            # Optional: Ensure the success url also respects the namespace
            success_url="/core/auth/password-reset/done/"
        ),
        name="password_reset"
    ),


    path(
        "auth/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="core/registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "auth/password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="core/registration/password_reset_confirm.html",
            success_url=reverse_lazy("core:password_reset_complete")
        ),
        name="password_reset_confirm"
    ),
    path(
        "auth/password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="core/registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

#-------------------------------------------------------------------------------------------------------------------
    # Team members
    path(
        "team-members/",
        TeamMemberListCreate.as_view(),
        name="team-member-list-create",
    ),
    path(
        "team-members/<int:pk>/",
        TeamMemberDetail.as_view(),
        name="team-member-detail",
    ),

    # Announcements
    path(
        "announcements/",
        AnnouncementListCreate.as_view(),
        name="announcement-list-create",
    ),
    path(
        "announcements/<int:pk>/",
        AnnouncementDetail.as_view(),
        name="announcement-detail",
    ),

    # Tags
    path(
        "tags/",
        TagListCreate.as_view(),
        name="tag-list-create",
    ),
    path(
        "tags/<int:pk>/",
        TagDetail.as_view(),
        name="tag-detail",
    ),

    # Events
    path(
        "events/",
        EventListCreate.as_view(),
        name="event-list-create",
    ),
    path(
        "events/<int:pk>/",
        EventDetail.as_view(),
        name="event-detail",
    ),

    # FanArt
    path(
        "fanart/",
        FanArtListCreate.as_view(),
        name="fanart-list-create",
    ),
    path(
        "fanart/<int:pk>/",
        FanArtDetail.as_view(),
        name="fanart-detail",
    ),

    # Seasonal reports
    path(
        "seasonal-reports/",
        SeasonalReportListCreate.as_view(),
        name="seasonal-report-list-create",
    ),
    path(
        "seasonal-reports/<int:pk>/",
        SeasonalReportDetail.as_view(),
        name="seasonal-report-detail",
    ),

    # Blog posts
    path(
        "blog-posts/",
        BlogPostListCreate.as_view(),
        name="blogpost-list-create",
    ),
    path(
        "blog-posts/<int:pk>/",
        BlogPostDetail.as_view(),
        name="blogpost-detail",
    ),

    # Fanfiction
    path(
        "fanfiction/",
        FanFictionListCreate.as_view(),
        name="fanfiction-list-create",
    ),
    path(
        "fanfiction/<int:pk>/",
        FanFictionDetail.as_view(),
        name="fanfiction-detail",
    ),

    # Chapters
    path(
        "fanfiction/<int:fanfic_id>/chapters/",
        ChapterListCreate.as_view(),
        name="chapter-list-create",
    ),
    path(
        "chapters/<int:pk>/",
        ChapterDetail.as_view(),
        name="chapter-detail",
    ),

    # Comments
    path(
        "comments/",
        CommentListCreate.as_view(),
        name="comment-list-create",
    ),
    path(
        "comments/<int:pk>/",
        CommentDetail.as_view(),
        name="comment-detail",
    ),

]

