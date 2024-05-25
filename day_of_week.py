from datetime import datetime

DOMINGO = 0

base_date = "2023-01-01"
base_DoW = DOMINGO

def calculate_days_from_base(date):
    # Converte as strings de data em objetos datetime
    
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(base_date, date_format)
    d2 = datetime.strptime(date, date_format)
    
    # Calcula a diferença entre as datas
    delta = d2 - d1
    
    # Retorna o número de dias de diferença
    return abs(delta.days)


def day_of_week(date: str) -> int:
    
    n_days = calculate_days_from_base(date)
    day_of_week_ = n_days % 7 # pelo facto da base date ser domingo (0) nao e preciso mais nada

    return day_of_week_
