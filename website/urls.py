from django.urls import path

from .views import IndexView
from .views import AboutView


urlpatterns = [
    path('',IndexView.as_view()),
    path('about/',AboutView.as_view()),
]
