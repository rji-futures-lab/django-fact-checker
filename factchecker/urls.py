from django.urls import include, path, re_path
from .views import index, detail


app_name = 'factchecker'
urlpatterns = [
    # ex: /factchecker/
    path('', index, name='index'),
    # ex: /factchecker/5/
    path('<int:claim_review_id>/', detail, name='detail'),
]
