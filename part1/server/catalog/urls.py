from django.urls import path

from .views import WinesView

urlpatterns = [
    path('wines/', WinesView.as_view()),
]
