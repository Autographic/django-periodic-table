"""django_periodic_table URL Configuration"""
from django.conf.urls import url
from .views import IndexView

urlpatterns = [
    url(r'^/', IndexView.as_view(), name="periodic_table"),
]
