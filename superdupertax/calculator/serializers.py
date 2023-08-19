# serializers.py
from rest_framework import serializers

from calculator.models import Report, Transaction


class ReportCalculationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    gross_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Report
        fields = '__all__'


class TransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    transaction_type = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    memo = serializers.CharField(max_length=500)


class ReportSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    transactions = TransactionSerializer(many=True, write_only=True)

    def create(self, validated_data):
        rows = validated_data.get('transactions')
        uuid = validated_data.get('uuid')
        name = validated_data.get('name')

        # Calculate expenses, gross_revenue, and transactions
        # could be more efficient, but its more understandable this way
        expenses = sum(row['amount'] for row in rows if row['transaction_type'].lower().strip() == 'expense')
        gross_revenue = sum(row['amount'] for row in rows if row['transaction_type'].lower().strip() == 'income')
        net_revenue = gross_revenue - expenses

        # Create the Report object
        report = Report.objects.create(
            uuid=uuid,
            name=name,
            expenses=expenses,
            gross_revenue=gross_revenue,
            net_revenue=net_revenue
        )

        # Create and bulk insert transactions
        transactions = [Transaction(report=report, **row) for row in rows]
        Transaction.objects.bulk_create(transactions)
        return report

    class Meta:
        model = Report
        fields = ['uuid', 'name', 'transactions']
