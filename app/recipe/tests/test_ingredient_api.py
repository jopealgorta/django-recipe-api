from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
    """Test the publicly available ingredients API"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test the private ingredients API"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.io', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Cucumber')
        Ingredient.objects.create(user=self.user, name='Onion')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that the ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(email='test2@example.io', password='test123')
        ingredient1 = Ingredient.objects.create(user=user2, name='Cucumber')
        ingredient2 = Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient2.name)
        self.assertNotIn(ingredient1, res.data)

    def test_create_ingredient_successful(self):
        """Test that ingredients are created successfully"""
        payload = {'name': 'Vinegar'}
        res = self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(user=self.user, name='Vinegar').exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_create_ingredient_invalid(self):
        """Test creating ingredient with invalid input data"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)