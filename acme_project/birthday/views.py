# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BirthdayForm
from .models import Birthday

from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    ...


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    ...


class BirthdayDeleteView(BirthdayMixin, DeleteView):  # type: ignore[misc]
    template_name = 'birthday/birthday_confirm_delete.html'


class BirthdayListView(ListView):
    model = Birthday
    # Explicit is better than implicit
    template_name = 'birthday/birthday_list.html'
    ordering = 'id'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # In case, there's a need & it looks like a setter rather
        context = super().get_context_data(**kwargs)
        context['try_for_fun'] = 'Hi from get_context_data()'
        return context


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    # Если был получен GET-запрос, отображаем форму
    return render(request, 'birthday/birthday.html', context)


def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(
        request.POST or None, files=request.FILES or None, instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


# def birthday_list(request):
#     birthdays = Birthday.objects.order_by('id')
#     paginator = Paginator(birthdays, 3)
#     page_num = request.GET.get('page')
#     page_obj = paginator.get_page(page_num)
#     return render(
#         request,
#         'birthday/birthday_list.html',
#         {'page_obj': page_obj}
#     )
