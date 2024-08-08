from datetime import datetime


def get_current_season(date=None):
    if date is None:
        date = datetime.now()
    month = date.month

    if 1 <= month <= 3:
        return "Winter"
    elif 4 <= month <= 6:
        return "Spring"
    elif 7 <= month <= 9:
        return "Summer"
    elif 10 <= month <= 12:
        return "Fall"
    else:
        return "Unknown"


# Contoh penggunaan
current_season = get_current_season()
print(f"Current anime season: {current_season}")
