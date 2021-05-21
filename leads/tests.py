from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.
class LandingPageTest(TestCase):

    # def test_status_code(self):
    #     response = self.client.get(reverse("landingpage"))
    #     self.assertEqual(response.status_code,200)
    #     self.assertTemplateUsed(response,"landingpage.html")

    # def test_template_name(self):
    #     response = self.client.get(reverse("landingpage"))
    #     self.assertTemplateUsed(response,"landingpage.html")
    def test_get(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landingpage.html")
