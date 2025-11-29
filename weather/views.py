from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import City, Subscription
from .openweather import OpenWeatherClient
from .serializers import CitySerializer, SubscriptionSerializer


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Get current weather by city name',
        tags=['weather'],
        responses={200: CitySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    operation_summary='Get a list of your subscriptions',
    operation_description='Returns all subscriptions of the currently logged in user.',
    tags=['subscriptions'],
    responses={200: SubscriptionSerializer(many=True)},
)
@swagger_auto_schema(
    method='post',
    operation_summary='Create a new city subscription',
    operation_description=(
        'Creates a subscription to receive weather information for the selected city.'
    ),
    tags=['subscriptions'],
    request_body=SubscriptionSerializer,
    responses={201: SubscriptionSerializer, 400: 'Bad Request'},
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def subscription_list_create(request):
    if request.method == 'GET':
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SubscriptionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = SubscriptionSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return Subscription.objects.filter(user=self.request.user)
class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary='Get a subscription by ID',
        tags=['subscriptions'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Renew the subscription completely',
        tags=['subscriptions'],
        request_body=SubscriptionSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partially renew the subscription',
        tags=['subscriptions'],
        request_body=SubscriptionSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Remove the subscription',
        tags=['subscriptions'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


weather_by_city_param = openapi.Parameter(
    name='city',
    in_=openapi.IN_QUERY,
    description='Name of the city (example, Tokyo или London,UK)',
    type=openapi.TYPE_STRING,
    required=True,
)

weather_response_manual = openapi.Response(
    description='Текущая погода от OpenWeatherMap',
    examples={
        'application/json': {
            'city': 'Moscow',
            'temp': 25.4,
            'feels_like': 24.8,
            'description': 'clear sky',
        }
    },
)


@swagger_auto_schema(
    method='get',
    operation_summary='Get the current weather in the city',
    operation_description='Returns current weather by city name via OpenWeatherMap.',
    tags=['weather'],
    manual_parameters=[weather_by_city_param],
    responses={
        200: weather_response_manual,
        400: openapi.Response('The city parameter is required.'),
        500: openapi.Response('Weather service error'),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather_by_city(request):
    city = request.query_params.get('city')
    if not city:
        return Response({'error': 'City parameter is required'}, status=400)
    try:
        client = OpenWeatherClient(settings.OPENWEATHER_API_KEY)
        data = client.get_weather(city)
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
