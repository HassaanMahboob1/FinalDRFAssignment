from django.urls import path
from rest_framework.routers import DefaultRouter
from notes.api_v1 import views
from .views import RegisterUserAPIView, NotesViewSet, ArchiveViewSet, shared

router = DefaultRouter()
router.register("Notes", NotesViewSet, basename="Notes")
router.register("archive", ArchiveViewSet, basename="Notes")
urlpatterns = [
    path("register", RegisterUserAPIView.as_view(), name="register"),
    path("shared", views.shared, name="shared"),
] + router.urls
