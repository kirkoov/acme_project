# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):  # Overrriding is for the sake on inserting
        # the current user as the author of the new post/birthday under way.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме:
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась:
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    # template_name = 'birthday/birthday_confirm_delete.html'
    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась:
        return super().dispatch(request, *args, **kwargs)


class BirthdayListView(ListView):
    model = Birthday
    # template_name = 'birthday/birthday_list.html'
    # По умолчанию этот класс выполняет запрос
    # queryset = Birthday.objects.all(), но мы его переопределим,
    # чтобы «снизить стоимость» получения объектов, связанных
    # «многие-ко-многим» (birthdays-tags), а заодно сократим и запросы
    # по методу «один-ко-многим» (Birthday и User), используя
    # select_related, = было 15 запросов, стало 3 - при 11 записях в БД!
    queryset = Birthday.objects.prefetch_related(
        'tags').select_related('author')
    ordering = 'id'
    paginate_by = 10


class BirthdayDetailView(DetailView):
    model = Birthday
    # template_name = 'birthday/birthday_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


# @login_required
# def add_comment(request, pk):
#     birthday = get_object_or_404(Birthday, pk=pk)
#     form = CongratulationForm(request.POST)
#     if form.is_valid():
#         # Создаём объект поздравления, но не сохраняем его в БД.
#         congratulation = form.save(commit=False)
#         # В поле author передаём объект автора поздравления.
#         congratulation.author = request.user
#         # В поле birthday передаём объект дня рождения.
#         congratulation.birthday = birthday
#         # Сохраняем объект в БД.
#         congratulation.save()
#     # Перенаправляем пользователя назад, на страницу дня рождения.
#     return redirect('birthday:detail', pk=pk)


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
