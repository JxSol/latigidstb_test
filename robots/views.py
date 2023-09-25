import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .messages import JSON_400, ROBOT_201
from .models import Robot


@method_decorator(csrf_exempt, name="dispatch")
class CreateRobotView(CreateView):
    """
    Создаёт Robot с данными из запроса.

    Методы:
        - POST
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
