# views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from calculator.models import Report
from calculator.serializers import ReportSerializer, ReportCalculationSerializer
import pandas as pd
from uuid import uuid4
from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_spectacular.utils import extend_schema


@extend_schema(responses=ReportSerializer)
@api_view(['GET'])
def all_reports(request):
    """Retrieve the names and uuids of all saved reports"""
    reports = Report.objects.all()
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)


@extend_schema(responses=ReportCalculationSerializer)
@api_view(['GET'])
def report(request, uuid):
    """Retrieve tax data for a specific report"""
    report = get_object_or_404(Report, uuid=uuid)

    serializer = ReportCalculationSerializer(report)
    return Response(serializer.data)


@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'file',
                    'format': 'binary'
                },
                'name': {
                    'type': 'string',
                }
            },
            'required': ['file', 'name']
        }
    },
    responses={201: ReportSerializer}
)
@api_view(['POST'])
def transactions(request):
    """Post a new .csv file with transactions made"""
    column_names = ['date', 'transaction_type', 'amount', 'memo']
    uploaded_file = request.FILES.get('file')

    # This is the most vulnerable part of the code, user input can be amazingly bad sometimes
    # Check if the uploaded file is empty
    if isinstance(uploaded_file, InMemoryUploadedFile) and uploaded_file.size == 0:
        return Response({"error": "Empty file. Please provide a file with content."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Try reading the file using pandas to check its format
    try:
        df = pd.read_csv(uploaded_file, names=column_names, header=0)
    except pd.errors.ParserError:
        return Response({"error": "Invalid file format. Please provide a valid CSV file."},
                        status=status.HTTP_400_BAD_REQUEST)

    df = df.dropna()
    report_data = {
        'name': request.data.get('name'),
        'uuid': uuid4(),
        'transactions': df.to_dict('records')
    }
    report_serializer = ReportSerializer(data=report_data)
    report_serializer.is_valid(raise_exception=True)
    report_serializer.save()

    return Response(report_serializer.data, status=status.HTTP_201_CREATED)
