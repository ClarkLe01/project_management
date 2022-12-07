from celery.utils.log import get_task_logger
import requests
from utils.models import Currency
from project.models import Project
from datetime import datetime
from celery import shared_task

logger = get_task_logger(__name__)


@shared_task
def updated_currency_exchange_rate():
    codes = {code.get('base') for code in Project.objects.all().values('base')}  # noqa: 501
    url = 'https://api.currencyapi.com/v3/latest?apikey=j7Q0mrbuSZ5q0H3YNTFcu516OEiiYpTIUnvoJNxj'  # noqa: 501
    query_currency = 'currencies=' + '%2C'.join(list(codes))
    url = url + '&' + query_currency
    """
    Response data from API when calling is successful
    {
        'meta': {'last_updated_at': '2022-11-09T23:59:59Z'},
        'data': {
            'USD': {'code': 'USD', 'value': 1},
            'VND': {'code': 'VND', 'value': 24867.260712}
        }
    }
    """
    res = requests.get(url)
    if res.status_code == 200:
        body = res.json()
        for code in body['data'].keys():
            obj, created = Currency.objects.update_or_create(code=code, defaults=body['data'].get(code))  # noqa: 501
            if created:
                logger.info("Create new code {0} at {1}".format(code, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))  # noqa: 501
        logger.info("The Currency Data updated at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))  # noqa: 501
    else:
        logger.error("The Currency API Call failed at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))  # noqa: 501
