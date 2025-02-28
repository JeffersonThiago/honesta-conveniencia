from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    result_expires=86400,
)
app.autodiscover_tasks(["accounts.tasks"])

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")