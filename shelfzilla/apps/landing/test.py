from django.test import TestCase
from django.core.urlresolvers import reverse


class LandingForBetaTest(TestCase):
    def test_can_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_can_access_landing(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)

    def test_redirect_home_to_landing(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('landing'))
