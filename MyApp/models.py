from django.db import models


class Pet(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=Gender.choices)
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=30)
    date_registered = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.name} ({self.pet_type})"
