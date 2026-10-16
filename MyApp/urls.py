from django.urls import path

from .views import PetCreateView, PetDeleteView, PetListView, PetUpdateView

urlpatterns = [
    path("", PetListView.as_view(), name="index"),
    path("pets/", PetListView.as_view(), name="pet_list"),
    path("pets/add/", PetCreateView.as_view(), name="pet_create"),
    path("pets/<int:pk>/edit/", PetUpdateView.as_view(), name="pet_update"),
    path("pets/<int:pk>/delete/", PetDeleteView.as_view(), name="pet_delete"),
]
