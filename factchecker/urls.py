from django.urls import include, path, re_path
from .views import index, detail, about


app_name = 'factchecker'
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('<int:claim_review_id>/', detail, name='detail'),
]
