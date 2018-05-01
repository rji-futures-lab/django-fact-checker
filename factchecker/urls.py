from django.urls import include, path, re_path
from .views import (
    ClaimCreateView,
    ClaimRatingListView,
    ComingSoonView,
    PublishedClaimReviewDetailView,
    PublishedClaimReviewListView,
    ThanksView,
    TestIconsView,
)


app_name = 'factchecker'
urlpatterns = [
    path('about/', ClaimRatingListView.as_view(), name='about'),
    path('', PublishedClaimReviewListView.as_view(), name='index'),
    path(
        '<int:pk>/',
        PublishedClaimReviewDetailView.as_view(),
        name='detail'
    ),
    path('submit-claim/', ClaimCreateView.as_view(), name='submit_claim'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('coming-soon/', ComingSoonView.as_view(), name='coming_soon'),
    path('test-icons/', TestIconsView.as_view(), name='test_icons')
]
