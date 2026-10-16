from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Pet


class PetManagementTests(TestCase):
    def setUp(self):
        self.pet = Pet.objects.create(
            name="Milo",
            pet_type="Dog",
            breed="Beagle",
            age=3,
            gender=Pet.Gender.MALE,
            owner_name="Alex Rivera",
            contact_number="09171234567",
        )

    def test_pet_list_shows_registered_pet(self):
        response = self.client.get(reverse("pet_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milo")
        self.assertContains(response, "Alex Rivera")
        self.assertContains(response, self.pet.date_registered.strftime("%b"))
        self.assertContains(response, str(self.pet.date_registered.year))

    def test_pet_registry_shows_live_summary_counts(self):
        Pet.objects.create(
            name="Pip",
            pet_type="Bird",
            breed="Parakeet",
            age=1,
            gender=Pet.Gender.FEMALE,
            owner_name="Alex Rivera",
            contact_number="09171234567",
        )
        Pet.objects.create(
            name="Luna",
            pet_type="Cat",
            breed="Tabby",
            age=2,
            gender=Pet.Gender.FEMALE,
            owner_name="Sam Lee",
            contact_number="09180000000",
        )

        response = self.client.get(reverse("pet_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pet_count"], 3)
        self.assertEqual(response.context["owner_count"], 2)
        self.assertEqual(response.context["type_count"], 3)
        self.assertContains(response, "Every pet has a story.")

    def test_pet_can_be_created(self):
        response = self.client.post(
            reverse("pet_create"),
            {
                "name": "Luna",
                "pet_type": "Cat",
                "breed": "Domestic shorthair",
                "age": 2,
                "gender": Pet.Gender.FEMALE,
                "owner_name": "Sam Lee",
                "contact_number": "09180000000",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("pet_list"))
        luna = Pet.objects.get(name="Luna")
        self.assertEqual(luna.owner_name, "Sam Lee")
        self.assertEqual(luna.date_registered, date.today())
        self.assertContains(response, "Luna has been registered")
        self.assertContains(response, "Luna")

    def test_pet_can_be_updated(self):
        response = self.client.post(
            reverse("pet_update", args=[self.pet.pk]),
            {
                "name": "Milo",
                "pet_type": "Dog",
                "breed": "Beagle",
                "age": 4,
                "gender": Pet.Gender.MALE,
                "owner_name": "Alex Rivera",
                "contact_number": "09171234567",
            },
        )

        self.assertRedirects(response, reverse("pet_list"))
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.age, 4)

    def test_pet_can_be_deleted(self):
        response = self.client.post(reverse("pet_delete", args=[self.pet.pk]))

        self.assertRedirects(response, reverse("pet_list"))
        self.assertFalse(Pet.objects.filter(pk=self.pet.pk).exists())

    def test_age_must_not_be_negative(self):
        response = self.client.post(
            reverse("pet_create"),
            {
                "name": "Negative",
                "pet_type": "Dog",
                "breed": "Unknown",
                "age": -1,
                "gender": Pet.Gender.MALE,
                "owner_name": "Sam Lee",
                "contact_number": "09180000000",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Pet.objects.filter(name="Negative").exists())

    def test_pet_form_does_not_include_a_photo_upload(self):
        response = self.client.get(reverse("pet_create"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'type="file"')
        self.assertNotContains(response, "Choose a pet photo")
        self.assertNotContains(response, 'class="topbar-meta"')
