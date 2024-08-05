from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.models import Restaurant, MenuItem
from restaurant.serializers import (
    RestaurantSerializer,
    MenuItemSerializer,
    MenuItemCreateSerializer,
    VoteSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()

    def get_queryset(self):
        today = timezone.now().date()
        restaurants_with_today_menu = (
            Restaurant.objects.filter(menu_items__data__date=today)
            .distinct()
            .order_by("-votes")[:1]
        )
        return restaurants_with_today_menu  # always return restaurant with most votes to get current dat result and day menu

    def get_serializer_class(self):
        serializer_class = RestaurantSerializer

        if self.action == "create":
            serializer_class = MenuItemCreateSerializer

        return serializer_class


class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = MenuItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class VoteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            restaurant = serializer.validated_data["restaurant"]
            restaurant.votes += 1
            restaurant.save()
            return Response(
                {"success": "Vote has been added."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
