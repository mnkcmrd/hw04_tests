import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    current_year = datetime.date.today().year
    return {
        'year': int(current_year)
    }
