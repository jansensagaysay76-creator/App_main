from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import PetForm
from .models import Pet


class PetListView(ListView):
    model = Pet
    template_name = "pet_list.html"
    context_object_name = "pets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pet_count"] = self.object_list.count()
        context["owner_count"] = (
            self.object_list.order_by().values("owner_name").distinct().count()
        )
        context["type_count"] = (
            self.object_list.order_by().values("pet_type").distinct().count()
        )
        return context


class PetCreateView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pet_form.html"
    success_url = reverse_lazy("pet_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"{self.object.name} has been registered and added to your pet list.",
        )
        return response


class PetUpdateView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "pet_form.html"
    success_url = reverse_lazy("pet_list")


class PetDeleteView(DeleteView):
    model = Pet
    template_name = "pet_confirm_delete.html"
    success_url = reverse_lazy("pet_list")
