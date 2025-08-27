from django.urls import path
from django.views.generic import DetailView, TemplateView

from .models import TestModel

urlpatterns = [
    path("", TemplateView.as_view(template_name="example.html"), name="example"),
    path("<pk>/", DetailView.as_view(model=TestModel), name="example_detail"),
]
