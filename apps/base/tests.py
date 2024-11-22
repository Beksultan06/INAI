from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.base.models import Product, Order, OrderProduct
from apps.users.models import User


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product",
            descriptions="Test Description",
            price=100
        )

    def test_product_creation(self):
        self.assertEqual(self.product.title, "Test Product")
        self.assertEqual(self.product.price, 100)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.product = Product.objects.create(
            title="Test Product",
            descriptions="Test Description",
            price=100
        )
        self.order = Order.objects.create(
            user=self.user,
            status="new",
            details="Test Order Details"
        )
        self.order_product = OrderProduct.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )

    def test_order_total_price(self):
        self.assertEqual(self.order.total_price, 200)

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Заказ {self.order.id} - new")


class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpassword")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.admin_token = self.get_jwt_token(self.admin_user)
        self.user_token = self.get_jwt_token(self.user)
        self.product = Product.objects.create(
            title="Test Product",
            descriptions="Test Description",
            price=100
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_product_list(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_product_create_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "New Product",
            "descriptions": "New Description",
            "price": 150,
        }
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_create_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "title": "Unauthorized Product",
            "descriptions": "Should Fail",
            "price": 150,
        }
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, 403)


class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = self.get_jwt_token(self.user)
        self.product = Product.objects.create(
            title="Test Product",
            descriptions="Test Description",
            price=100
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_order_creation(self):
        data = {
            "status": "new",
            "details": "Test Order",
            "order_products": [
                {"product": self.product.id, "quantity": 3}
            ]
        }
        response = self.client.post("/api/orders/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
