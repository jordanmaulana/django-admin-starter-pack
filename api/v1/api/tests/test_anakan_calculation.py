from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.calculations.models import Calculation
from apps.products.models import Product


class AnakanCalculationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        # Create a dummy image for the product
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b",
            content_type="image/jpeg",
        )
        self.roof_product = Product.objects.create(
            name="Test Roof",
            type="roof",
            price=100,
            actor=self.user,
            coefficient=1.1,
            image=image,
        )

    def test_create_calculation_with_anakan(self):
        url = reverse("calculation-list-create")
        data = {
            "shape": "Pelana",
            "lebar": 15,
            "panjang": 25,
            "overhang": 1,
            "tilt": 35,
            "calculate_roof": True,
            "roof_uid": self.roof_product.uid,
            "anakans": [
                {
                    "lebar": 5,
                    "panjang": 10,
                    "overhang": 3,
                    "tilt": 30,
                }
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Calculation.objects.count(), 2)
        main_calculation = Calculation.objects.get(parent__isnull=True)
        anakan_calculation = Calculation.objects.get(parent__isnull=False)
        self.assertEqual(anakan_calculation.parent, main_calculation)
        self.assertEqual(main_calculation.items.count(), 1)
        self.assertEqual(anakan_calculation.items.count(), 1)

    def test_anakan_image_url_is_absolute(self):
        """Verify that the image URL in the anakan is absolute"""
        # Create a calculation with an anakan
        url = reverse("calculation-list-create")
        data = {
            "shape": "Pelana",
            "lebar": 15,
            "panjang": 25,
            "overhang": 1,
            "tilt": 35,
            "calculate_roof": True,
            "roof_uid": self.roof_product.uid,
            "anakans": [
                {
                    "lebar": 5,
                    "panjang": 10,
                    "overhang": 3,
                    "tilt": 30,
                }
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the main calculation id from the response
        main_calculation_id = response.data["uid"]

        # Retrieve the calculation detail
        detail_url = reverse(
            "calculation-retrieve-update-destroy", kwargs={"uid": main_calculation_id}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the image URL in the anakan
        anakan = response.data["anakans"][0]
        product_item = anakan["materials"][0]
        self.assertTrue(product_item["product"]["image"].startswith("http"))
