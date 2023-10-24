from unittest import TestCase
from rest_framework.test import APIClient


class TestSomething(TestCase):
    def test_StockViewSet(self):
        client = APIClient()
        response = client.get('/api/v1/stocks/')
        self.assertEqual(response.status_code, 200)
