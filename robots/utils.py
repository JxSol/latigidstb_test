from openpyxl import Workbook

from robots.paginators import RobotModelPaginator


def generate_workbook(
        fields: tuple | list,
        col_names: tuple | list,
        paginator: RobotModelPaginator,
):
    """
    Заполняет Workbook данными

    Params:
        - fields - поля модели, данными из которых заполняются таблицы.
        - col_names - заголовки для колонок таблиц.
        - paginator - пагинатор, откуда будут браться страницы.
    """
    wb = Workbook()
    wb.remove(wb.active)
    for page in paginator:
        ws = wb.create_sheet(title=f'{str(page)}')
        ws.append(col_names)
        for item in page:
            ws.append([item.get(field_name, '') for field_name in fields])
    return wb
