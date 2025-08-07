from datetime import timedelta

def get_days_in_range(start_date, end_date):
    """Return a set of weekday names inside the given date range."""
    days = set()
    current_date = start_date
    while current_date <= end_date:
        days.add(current_date.strftime("%A").lower())  # e.g., "monday"
        current_date += timedelta(days=1)
    return days


def gallery_is_open_for_range(gallery, days_in_range):
    """Return True if gallery is open for all days in the range."""
    if gallery.days_closed:
        closed_days = {d.strip().lower() for d in gallery.days_closed.split(",")}
        if closed_days & days_in_range:  # intersection → closed at least 1 day
            return False
    return True
