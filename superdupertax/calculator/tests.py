from django.test import TestCase

from calculator.models import Report
from calculator.serializers import ReportSerializer
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


class ReportSerializerTests(TestCase):
    def test_create_report(self):
        # Test data for the ReportSerializer
        report_data = {
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'name': 'Test Report',
            'transactions': [
                {'date': '2023-07-27', 'transaction_type': 'Income',
                    'amount': 500.00, 'memo': 'Test income'},
                {'date': '2023-07-28', 'transaction_type': 'Expense',
                    'amount': 100.00, 'memo': 'Test expense'},
            ]
        }

        # Create the serializer with the test data
        serializer = ReportSerializer(data=report_data)

        # Check if the data is valid
        self.assertTrue(serializer.is_valid())

        # Call the create method and check if it creates a Report object
        report = serializer.create(serializer.validated_data)
        self.assertIsNotNone(report)
        self.assertEqual(report.name, 'Test Report')
        self.assertEqual(report.expenses, 100.00)
        self.assertEqual(report.gross_revenue, 500.00)
        self.assertEqual(report.net_revenue, 400.00)

        # Check if the transactions are saved correctly
        transactions = report.transactions.all()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].date, '2023-07-27')
        self.assertEqual(transactions[0].transaction_type, 'Income')
        self.assertEqual(transactions[0].amount, 500.00)
        self.assertEqual(transactions[0].memo, 'Test income')

    def test_create_report_with_no_transactions(self):
        # Test data without any transactions
        report_data = {
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'name': 'Test Report',
            'transactions': []
        }

        serializer = ReportSerializer(data=report_data)
        self.assertTrue(serializer.is_valid())

        # Call the create method and check if it creates a Report object
        report = serializer.create(serializer.validated_data)
        self.assertIsNotNone(report)
        self.assertEqual(report.name, 'Test Report')
        self.assertEqual(report.expenses, 0.00)
        self.assertEqual(report.gross_revenue, 0.00)
        self.assertEqual(report.net_revenue, 0.00)

        # Check if no transactions are saved
        transactions = report.transactions.all()
        self.assertEqual(len(transactions), 0)

    def test_create_report_with_invalid_transaction(self):
        # Test data with an invalid transaction (missing 'amount' field)
        report_data = {
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'name': 'Test Report',
            'transactions': [
                {'date': '2023-07-27', 'transaction_type': 'Income',
                    'memo': 'Test income'}
            ]
        }

        serializer = ReportSerializer(data=report_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('transactions', serializer.errors)
        self.assertIn('amount', serializer.errors['transactions'][0])


class TransactionsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_report_with_empty_file(self):
        # Test data with an empty file
        empty_file = SimpleUploadedFile("empty.csv", b"")

        response = self.client.post(
            '/transactions/',
            {
                'name': 'Empty File Report',
                'file': empty_file
            },
            format='multipart'
        )

        # The response should be a bad request since the file is empty
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the report was not created
        report_count = Report.objects.count()
        self.assertEqual(report_count, 0)
