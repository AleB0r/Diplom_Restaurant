from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from twilio.rest import Client

from reservations.models import Reservation

account_sid = 'AC417af06a5571ac88b40df63201df6f16'
auth_token = '65f4049a88668140c3d0190d404a0979'
client = Client(account_sid, auth_token)

@shared_task
def send_sms(phone_number, message_body):
    message = client.messages.create(
        body=message_body,
        from_='+12565783816',
        to=phone_number
    )
    return message.sid

def check_reservations_and_send_sms():
    now = timezone.now()
    later = now + timedelta(minutes=30)

    reservations = Reservation.objects.filter(reservation_time__range=(now, later))

    for reservation in reservations:
        if reservation.client.phone_number:
            message_body = f'Dear {reservation.client.first_name}, you have reserved table No.{reservation.table.number} at {reservation.reservation_time}.'
            send_sms(reservation.client.phone_number, message_body)


from celery import shared_task

@shared_task
def send_reservation_reminders():
    check_reservations_and_send_sms()
