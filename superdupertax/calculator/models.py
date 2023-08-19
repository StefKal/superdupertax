from uuid import uuid4
from django.db import models


class Report(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)

    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    gross_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    net_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        default_related_name = 'reports'


class Transaction(models.Model):
    date = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.CharField(max_length=255)
    report = models.ForeignKey(
        Report, related_name="transactions", on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'transactions'
