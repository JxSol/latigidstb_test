import json

from django.db.models import Count
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from .messages import JSON_400
from .models import Robot
from .paginators import RobotModelPaginator
from .utils import generate_workbook


@method_decorator(csrf_exempt, name="dispatch")
class CreateRobotView(CreateView):
    """
    Создаёт Robot с данными из запроса.

    Методы:
        - POST
    Тело запроса:
        JSON
    """
    model = Robot
    fields = (
        'model',
        'version',
        'created',
    )

    def post(self, request, *args, **kwargs):
        """Добавляем загрузку JSON из тела запроса."""
        try:
            self.kwargs['json_data'] = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'detail': JSON_400}, status=400)
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Переопределяем источник данных для формы на json в теле запроса."""
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.kwargs.get('json_data')
        return kwargs

    def form_valid(self, form):
        """Переопределяем успешный ответ."""
        self.object = form.save()
        return JsonResponse(model_to_dict(self.object), status=201)

    def form_invalid(self, form):
        """Переопределяем неуспешный ответ."""
        super().form_invalid(form)
        return JsonResponse({'detail': form.errors}, status=400)


class ProductionWeekReport(ListView):
    """
    Формирует Excel-отчёт по созданию роботов за последнюю неделю.

    Форма отчёта:
        Модель | Версия | Количество за неделю
    Пагинация по моделям.
    """
    # день, с которого начинается отчёт
    date_from = timezone.now() - timezone.timedelta(days=7)
    filename = f'robot-production-week-report-{date_from.date()}.xlsx'

    queryset = (
        Robot.objects
        .filter(created__gte=date_from)
        .values('model', 'version')
        .annotate(counter=Count('*'))
    )
    fields = {
        'model': 'Модель',
        'version': 'Версия',
        'counter': 'Количество за неделю'
    }
    paginator_class = RobotModelPaginator
    response_class = HttpResponse
    content_type = 'application/vnd.ms-excel'

    def render_to_response(self, context, **response_kwargs):
        """Переопределяем рендеринг данных для ответа."""
        response_kwargs.setdefault("content_type", self.content_type)
        wb = generate_workbook(
            list(self.fields.keys()),
            list(self.fields.values()),
            self.paginator_class(self.queryset),
        )
        response = self.response_class(**response_kwargs)
        response[
            'Content-Disposition'] = f'attachment; filename={self.filename}'
        wb.save(response)
        return response
