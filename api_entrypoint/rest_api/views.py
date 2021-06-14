import ipdb
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Trip
from .serializers import TripSerializer


LOG_INTO_DB = False


class TripViewSet(viewsets.ModelViewSet):
    """
        API ViewSet for Trip model
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):

    #     if LOG_INTO_DB:
    #         return Response({
    #             'logging_into_db': True,
    #             'number_of_datapoints': self.queryset.count()
    #         })
    #     else:
    #         return Response({
    #             'logging_into_db': False,
    #             'message': 'The datapoints are not being logged locally.'
    #         })


class TripAPIView(APIView):
    """
        API View for Trip model
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request, *args, **kwargs):

        if LOG_INTO_DB:
            return Response({
                'logging_into_db': True,
                'number_of_datapoints': self.queryset.count()
            })
        else:
            return Response({
                'logging_into_db': False,
                'message': 'The datapoints are not being logged locally.'
            })

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        assert False, f'Validated data {serializer.validated_data}'
        if serializer.is_valid():
            print(serializer.validated_data['origin_coord'])

            if LOG_INTO_DB:
                serializer.save()
            return Response({'success': True})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
