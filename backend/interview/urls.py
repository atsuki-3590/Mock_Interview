from django.urls import path
from . import api_views
from django.views.generic import TemplateView

urlpatterns = [
    path("api/upload_pdf/", api_views.api_upload_pdf),
    path("api/send_answer/", api_views.api_send_answer),
    path("api/next_question/", api_views.api_next_question),
    path("google5124318fd1b3da6d.html", TemplateView.as_view(template_name="google5124318fd1b3da6d.html")),
]