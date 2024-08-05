from django.utils import timezone
from rest_framework import serializers
from restaurant.models import Restaurant, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    restaurant = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = MenuItem
        fields = ("id", "data", "dish_name", "price", "restaurant")

    def get_data(self, obj):
        if obj.data:
            return obj.data.strftime("%d/%m/%Y")
        return None

    def create(self, validated_data):
        return MenuItem.objects.create(**validated_data)


class MenuItemCreateSerializer(serializers.Serializer):
    restaurant = serializers.SlugRelatedField(
        slug_field="name", queryset=Restaurant.objects.all()
    )
    menu_items = serializers.ListField(child=MenuItemSerializer())

    def create(self, validated_data):
        restaurant = validated_data["restaurant"]
        menu_items_data = validated_data["menu_items"]
        menu_items = [
            MenuItem(restaurant=restaurant, **item) for item in menu_items_data
        ]
        return MenuItem.objects.bulk_create(menu_items)


class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "address",
            "votes",
            "menu_items",
        )

    def get_menu_items(self, obj):
        today = timezone.now().date()
        menu_items = obj.menu_items.filter(data__date=today)
        return MenuItemSerializer(menu_items, many=True).data

    def create(self, validated_data):
        menu_items_data = validated_data.pop("menu_items", [])
        restaurant = Restaurant.objects.create(**validated_data)
        for menu_item_data in menu_items_data:
            MenuItem.objects.create(restaurant=restaurant, **menu_item_data)
        return restaurant

    def update(self, instance, validated_data):
        menu_items_data = validated_data.pop("menu_items", [])

        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.save()

        if menu_items_data:
            instance.menu_items.all().delete()
            for menu_item_data in menu_items_data:
                MenuItem.objects.create(restaurant=instance, **menu_item_data)

        return instance


class VoteSerializer(serializers.Serializer):
    restaurant = serializers.SlugRelatedField(
        slug_field="name", queryset=Restaurant.objects.all()
    )
