from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    # template_name = 'birthday/birthday_confirm_delete.html'
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayListView(ListView):
    model = Birthday
    # template_name = 'birthday/birthday_list.html'
    ordering = 'id'
    paginate_by = 3


class BirthdayDetailView(DetailView):
    model = Birthday
    # template_name = 'birthday/birthday_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context
