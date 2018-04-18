from django.urls import include, path, re_path
from .views import (
    index,
    detail,
    about,
    submit_claim,
    thanks,
    coming_soon,
)


app_name = 'factchecker'
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('<int:claim_review_id>/', detail, name='detail'),
    path('submit-claim/', submit_claim, name='submit_claim'),
    path('thanks/', thanks, name='thanks'),
    path('coming-soon/', coming_soon, name='coming_soon')
]
