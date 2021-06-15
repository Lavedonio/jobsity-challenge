from copy import deepcopy
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .aux import kafka_produce
from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    """
        API ViewSet for Trip model
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    # Disabled for this challenge
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    authentication_classes = []
    permission_classes = []


class StatusAPIView(APIView):
    """
        API View for diplaying status info of the project
    """
    # Disabled for this challenge
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        status = {}
        status_mapper = {}
        for key, value in Trip.STATUS_CHOICES:
            status_mapper[key] = value

        queryset = Trip.objects.values('status') \
            .annotate(total=Count('status')) \
            .order_by()

        for status_count in queryset:
            status[status_mapper[status_count['status']]
                   ] = status_count['total']

        try:
            assert status[status_mapper[Trip.PROCESSED_ERROR]] > 0
        except (AssertionError, KeyError):
            try:
                assert status[status_mapper[Trip.WAITING]] > 0
            except (AssertionError, KeyError):
                try:
                    assert status[status_mapper[Trip.PROCESSING]] > 0
                except (AssertionError, KeyError):
                    message = "All data was processed."
                else:
                    message = "There are data being processed."
            else:
                message = "There are data that are waiting to be processed."
        else:
            message = "All data was processed, but some failed."

        info = {
            'status': 'OK',
            'message': message,
            'trip_status': status
        }

        return Response(info)

    def post(self, request, *args, **kwargs):
        print(request.data)

        status_mapper = {}
        for value, key in Trip.STATUS_CHOICES:
            status_mapper[key] = value

        reprocess_status = []
        for status_type in request.data['reprocess']:
            try:
                converted_status = status_mapper[status_type]
            except KeyError:
                pass
            else:
                reprocess_status.append(converted_status)

        qs = Trip.objects.filter(status__in=reprocess_status)

        for obj in qs:
            obj_dict = deepcopy(obj.__dict__)

            unwanted_fields = ['id', 'status',
                               'created_at', 'updated_at', '_state']
            for field in unwanted_fields:
                del obj_dict[field]

            obj_dict['date_time'] = str(obj_dict['date_time'])
            kafka_key = obj_dict['hash_value']
            del obj_dict['hash_value']

            print(obj_dict)
            kafka_produce(kafka_key, obj_dict)

        return Response({
            'message': 'Trips with status waiting are being reprocessed.'
        })


{
    "reprocess": ["Waiting"]
}
