from celery import shared_task
from restaurant.models import Restaurant


@shared_task
def reset_votes():
    Restaurant.objects.update(votes=0)
