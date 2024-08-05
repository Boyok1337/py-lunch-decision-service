from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurant.views import RestaurantViewSet, MenuItemViewSet, VoteAPIView

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurants")
router.register("menu", MenuItemViewSet, basename="menu")

urlpatterns = [
    path("", include(router.urls)),
    path("vote/", VoteAPIView.as_view(), name="vote"),
]

app_name = "restaurant"
