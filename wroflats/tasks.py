import random
from api import app
from time import sleep
from celery import Celery

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def scrape_index(self, target: str):
    """Scrapes an index of a specified target."""
    with app.app_context():
        #TODO: Refactor legacy code into asynchronous tasks
        pass

@celery.task(bind=True)
def scrape_single(self, target: str):
    """Scrapes a single submission to get more data."""
    with app.app_context():
        #TODO: Refactor legacy code into asynchronous tasks
        pass

@celery.task(bind=True)
def calculate_ratings(self):
    """Calculates ratings for recently added submissions."""
    with app.app_context():
        #TODO: Refactor legacy code into asynchronous tasks
        pass

@celery.task(bind=True)
def calculate_submissions(self):
    """Creates local instances of globally scraped read-only submissions."""
    with app.app_context():
        #TODO: Refactor legacy code into asynchronous tasks
        pass