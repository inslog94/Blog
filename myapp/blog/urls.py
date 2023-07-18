from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.Index.as_view(), name="list"),
    path("detail/<int:pk>/", views.PostDetail.as_view(), name="detail"),
    path("detail/<int:pk>/delete/", views.PostDelete.as_view(), name="delete"),
    path("search/", views.Search.as_view(), name="search"),
]
