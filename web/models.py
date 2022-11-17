import uuid

from django.db import models


class Connections(models.Model):
    connection_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dbtype = models.CharField(max_length=50, null=False)
    connection_name = models.CharField(max_length=50, null=False)
    host = models.CharField(max_length=50, null=False)
    port = models.IntegerField(default=3456, null=False)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    schema = models.CharField(max_length=50, null=True)
