from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.Index.as_view(), name="list"),
    path("detail/<int:pk>/", views.PostDetail.as_view(), name="detail"),
]
