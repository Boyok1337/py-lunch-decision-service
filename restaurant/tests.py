from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from restaurant.models import Restaurant, MenuItem
from django.utils import timezone

User = get_user_model()


class RestaurantMenuItemVoteTests(APITestCase):
    def setUp(self):
        # Створення користувача
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        today = timezone.now().date()
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            price=10.99,
            dish_name="Test Dish"  # Додайте dish_name
        )
        self.menu_item_url = reverse('restaurant:menu-list')
        self.restaurant_url = reverse('restaurant:restaurants-list')
        self.vote_url = reverse('restaurant:vote')

        self.valid_menu_item_payload = {
            'restaurant': self.restaurant.name,
            'menu_items': [
                {
                    'dish_name': 'New Test Dish',
                    'price': 9.99
                }
            ]
        }
        self.invalid_menu_item_payload = {
            'restaurant': self.restaurant.name,
            # Відсутнє поле 'price'
        }

        self.valid_vote_payload = {
            'restaurant': self.restaurant.name
        }
        self.invalid_vote_payload = {
            'restaurant': 9999
        }

        # Додати токен авторизації до клієнта
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_restaurant_with_today_menu(self):
        response = self.client.get(self.restaurant_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.restaurant.name)

    def test_create_menu_item(self):
        response = self.client.post(self.menu_item_url, self.valid_menu_item_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)
        self.assertEqual(MenuItem.objects.latest('id').restaurant, self.restaurant)

    def test_create_invalid_menu_item(self):
        response = self.client.post(self.menu_item_url, self.invalid_menu_item_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_success(self):
        response = self.client.post(self.vote_url, self.valid_vote_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.votes, 1)

    def test_vote_failure(self):
        response = self.client.post(self.vote_url, self.invalid_vote_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
