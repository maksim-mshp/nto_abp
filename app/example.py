from datetime import datetime

from utils import object_as_dict
from core.database import add_sample_data
from services.job import job_service
from services.event import event_service

add_sample_data()


def example():
    job = job_service.get_job_by_id(2)
    print(job)
    job_service.change_job_status(2, 'К работе')
    job = job_service.get_job_by_id(2)
    print(job)
    event = event_service.get_events('Просвещение')[0]
    job_room = job_service.create_job_room('комната')
    job_type = job_service.create_job_type('тип работы')
    job = job_service.create_job(
        'title',
        'desc',
        event['id'],
        job_type['id'],
        job_room['id'],
        datetime(2023, 12, 12),
        'К работе'
    )
    print(job)


example()
