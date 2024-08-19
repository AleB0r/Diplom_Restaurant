import os

from django.db.models import Sum, F, Count
from django.utils import timezone

from orders.models import Order, OrderDish

from celery import shared_task

@shared_task
def Hi():
    print('ho')

@shared_task
def generate_report():
    today = timezone.now().date()
    formatted_date = today.strftime('%Y-%m-%d')

    total_revenue = OrderDish.objects.filter(
        order__order_time__date=today
    ).values('dish').annotate(
        dish_price=Sum(F('quantity') * F('dish__price'))
    ).aggregate(
        total_revenue=Sum('dish_price')
    )['total_revenue'] or 0

    total_orders = Order.objects.filter(order_time__date=today).count()

    average_check = OrderDish.objects.filter(
        order__order_time__date=today
    ).values('order').annotate(
        order_total=Sum(F('quantity') * F('dish__price'))
    ).aggregate(
        average_check=Sum('order_total') / Count('order')
    )['average_check'] or 0

    report_content = (
        f"Отчет за {today}\n"
        f"Суммарная прибыль: {total_revenue:.2f} рублей\n"
        f"Количество заказов: {total_orders}\n"
        f"Средняя цена чека: {average_check:.2f} рублей\n"
    )

    report_filename = f"daily_report_{formatted_date}.txt"
    report_filepath = os.path.join('/home/alexborisevich/PycharmProjects/Diplom_Restaurant/reports', report_filename)

    with open(report_filepath, 'w') as report_file:
        report_file.write(report_content)

    print(f"Отчет сохранен в {report_filepath}")

