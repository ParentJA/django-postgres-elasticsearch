from rest_framework.test import APIClient, APITestCase

from catalog.models import Wine
from catalog.serializers import WineSerializer


class ViewTests(APITestCase):
    fixtures = ['test_wines.json']

    def setUp(self):
        self.client = APIClient()

    def test_empty_query_returns_everything(self):
        response = self.client.get('/api/v1/catalog/wines/')
        wines = Wine.objects.all()
        self.assertJSONEqual(response.content, WineSerializer(wines, many=True).data)

    def test_query_matches_variety(self):
        response = self.client.get('/api/v1/catalog/wines/?query=Cabernet')
        self.assertEquals(1, len(response.data))
        self.assertEquals("58ba903f-85ff-45c2-9bac-6d0732544841", response.data[0]['id'])

    def test_query_matches_winery(self):
        response = self.client.get('/api/v1/catalog/wines/?query=Barnard')
        self.assertEquals(1, len(response.data))
        self.assertEquals("21e40285-cec8-417c-9a26-4f6748b7fa3a", response.data[0]['id'])

    def test_query_matches_description(self):
        response = self.client.get('/api/v1/catalog/wines/?query=wine')
        self.assertEquals(3, len(response.data))
        self.assertCountEqual([
            "58ba903f-85ff-45c2-9bac-6d0732544841",
            "21e40285-cec8-417c-9a26-4f6748b7fa3a",
            "0082f217-3300-405b-abc6-3adcbecffd67",
        ], [item['id'] for item in response.data])

    def test_can_filter_on_country(self):
        response = self.client.get('/api/v1/catalog/wines/?country=France')
        self.assertEquals(1, len(response.data))
        self.assertEquals("0082f217-3300-405b-abc6-3adcbecffd67", response.data[0]['id'])

    def test_can_filter_on_points(self):
        response = self.client.get('/api/v1/catalog/wines/?points=87')
        self.assertEquals(1, len(response.data))
        self.assertEquals("21e40285-cec8-417c-9a26-4f6748b7fa3a", response.data[0]['id'])

    def test_country_must_be_exact_match(self):
        response = self.client.get('/api/v1/catalog/wines/?country=Frances')
        self.assertEquals(0, len(response.data))
        self.assertJSONEqual(response.content, [])
