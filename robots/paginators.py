from django.core.paginator import Page
import inspect
from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args


class RobotModelPaginator:
    """
    Пагинатор для модели Robot, который выделяет страницу
    для каждой уникальной Robot.model
    """

    def __init__(self, object_list):
        self.object_list = object_list
        self.models = (
            object_list
            .values_list('model', flat=True)
            .distinct()
            .order_by('model')
        )

    def __iter__(self):
        """Итерирует, возвращая страницы."""
        for page_number in self.page_range:
            model = self.models[page_number - 1]
            yield TitledPage(
                self.object_list.filter(model=model).order_by('version'),
                page_number,
                self,
                model,
            )

    @cached_property
    def num_pages(self) -> int:
        """Возвращает количество страниц."""
        c = getattr(self.models, "count", None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return c()
        return len(self.models)

    @property
    def page_range(self) -> range:
        """
        Возвращает диапазон страниц, начиная с 1, для итерации внутри цикла.
        """
        return range(1, self.num_pages + 1)


class TitledPage(Page):
    """Страница, имеющая заголовок."""

    def __init__(self, object_list, number, paginator, title=None):
        super().__init__(object_list, number, paginator)
        self.title = title

    def __repr__(self):
        if self.title:
            return self.title
        super().__repr__()
