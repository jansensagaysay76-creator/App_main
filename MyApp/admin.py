from django.contrib import admin

from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "pet_type",
        "breed",
        "age",
        "gender",
        "owner_name",
        "date_registered",
    )
    list_filter = ("pet_type", "gender", "date_registered")
    search_fields = ("name", "breed", "owner_name", "contact_number")
