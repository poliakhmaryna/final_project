from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    today = datetime.today().date()
    in_7_days = today + timedelta(days=7)
    upcoming = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        if today <= birthday_this_year <= in_7_days:
            congratulation_date = birthday_this_year
            if congratulation_date.weekday() == 5:  # Saturday
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:  # Sunday
                congratulation_date += timedelta(days=1)
            upcoming.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })
    return upcoming