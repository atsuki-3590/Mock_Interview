from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path("google5124318fd1b3da6d.html", TemplateView.as_view(template_name="google5124318fd1b3da6d.html")),
]