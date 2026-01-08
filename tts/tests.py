from django.test import TestCase

class HealthTest(TestCase):
    def test_home_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
