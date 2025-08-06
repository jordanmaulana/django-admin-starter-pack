from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.brands.models import Brand
from apps.products.models import Product


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.brand1 = Brand.objects.create(name="Brand A")
        self.brand2 = Brand.objects.create(name="Brand B")

        # Create some test products
        self.product1 = Product.objects.create(
            name="Roof Tile A", price=10000, type="roof", brand=self.brand1
        )
        self.product2 = Product.objects.create(
            name="Material X", price=5000, type="material", brand=self.brand2
        )
        self.product3 = Product.objects.create(
            name="Roof Tile B", price=12000, type="roof", brand=self.brand1
        )
        self.product4 = Product.objects.create(
            name="Material Y", price=7000, type="material", brand=self.brand2
        )
        self.product5 = Product.objects.create(
            name="Another Roof Tile", price=15000, type="roof", brand=self.brand1
        )

    def test_list_products(self):
        url = "/api/v1/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"]), 5)

    def test_list_products_filter_by_type(self):
        url = "/api/v1/products/?type=roof"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)
        for product_data in response.data["results"]:
            self.assertEqual(product_data["type"], "roof")

        url = "/api/v1/products/?type=material"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)
        for product_data in response.data["results"]:
            self.assertEqual(product_data["type"], "material")

    def test_list_products_search_by_name(self):
        url = "/api/v1/products/?name=Roof Tile"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)
        for product_data in response.data["results"]:
            self.assertIn("Roof Tile", product_data["name"])

        url = "/api/v1/products/?name=Material"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)
        for product_data in response.data["results"]:
            self.assertIn("Material", product_data["name"])

    def test_list_products_pagination(self):
        # Test default page size (10)
        url = "/api/v1/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        # Test page size 2
        url = "/api/v1/products/?page_size=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["count"], 5)

        # Test page 2 with page size 2
        url = "/api/v1/products/?page=2&page_size=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["count"], 5)
        # The order of products is based on name, so product4 (Material Y) and product1 (Roof Tile A) should be on the second page
        self.assertEqual(response.data["results"][0]["name"], self.product4.name)
        self.assertEqual(response.data["results"][1]["name"], self.product1.name)

    def test_product_brand_serialization(self):
        url = "/api/v1/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Find a product with a brand
        product_with_brand = None
        for product_data in response.data["results"]:
            if "brand" in product_data and product_data["brand"] is not None:
                product_with_brand = product_data
                break

        self.assertIsNotNone(
            product_with_brand, "No product with a brand found in the response."
        )
        self.assertIn("uid", product_with_brand["brand"])
        self.assertIn("name", product_with_brand["brand"])

        # Verify the brand data for a specific product
        if product_with_brand["name"] == self.product1.name:
            self.assertEqual(product_with_brand["brand"]["uid"], str(self.brand1.uid))
            self.assertEqual(product_with_brand["brand"]["name"], self.brand1.name)
        elif product_with_brand["name"] == self.product2.name:
            self.assertEqual(product_with_brand["brand"]["uid"], str(self.brand2.uid))
            self.assertEqual(product_with_brand["brand"]["name"], self.brand2.name)
