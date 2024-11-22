from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from datetime import timedelta

from apps.planning.models import Route, Vehicle
from apps.users.models import User
from apps.base.models import Order


class RouteViewSetTestCase(TestCase):
    def setUp(self):
        self.moto = Vehicle.objects.create(name="Мотоцикл Honda", license_plate="123-ABC", capacity=100, available=True)
        self.bike = Vehicle.objects.create(name="Велосипед", license_plate="456-DEF", capacity=50, available=True)

        couriers_group, created = Group.objects.get_or_create(name="Курьеры")
        self.courier1 = User.objects.create_user(username="courier1", password="password123")
        self.courier2 = User.objects.create_user(username="courier2", password="password456")
        self.courier1.groups.add(couriers_group)
        self.courier2.groups.add(couriers_group)

        self.order = Order.objects.create(user=self.courier1, status="new", details="Тестовый заказ")

        self.client = APIClient()
        self.client.force_authenticate(user=self.courier1)

    def test_vehicle_priority_selection(self):
        response = self.client.post("/api/v1/planning/routes/", {
            "order": self.order.id,
            "start_location": "Склад",
            "end_location": "Адрес клиента",
            "distance": 10,
            "estimated_time": "00:30:00"
        })
        self.assertEqual(response.status_code, 201)
        route = Route.objects.first()
        self.assertEqual(route.vehicle.name, "Мотоцикл Honda")
        self.moto.refresh_from_db()
        self.assertFalse(self.moto.available)

    def test_no_available_vehicle(self):
        Vehicle.objects.update(available=False)
        response = self.client.post("/api/v1/planning/routes/", {
            "order": self.order.id,
            "start_location": "Склад",
            "end_location": "Адрес клиента",
            "distance": 10,
            "estimated_time": "00:30:00"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Нет доступных транспортных средств.", str(response.data))

    def test_courier_selection(self):
        Route.objects.create(
            order=self.order,
            courier=self.courier1,
            vehicle=self.moto,
            start_location="A",
            end_location="B",
            distance=5,
            estimated_time=timedelta(minutes=15),
            status="in_progress"
        )
        response = self.client.post("/api/v1/planning/routes/", {
            "order": self.order.id,
            "start_location": "Склад",
            "end_location": "Адрес клиента",
            "distance": 10,
            "estimated_time": "00:30:00"
        })
        self.assertEqual(response.status_code, 201)
        route = Route.objects.last()
        self.assertNotEqual(route.courier, self.courier1)

    def test_mark_vehicle_as_unavailable(self):
        response = self.client.post("/api/v1/planning/routes/", {
            "order": self.order.id,
            "start_location": "Склад",
            "end_location": "Адрес клиента",
            "distance": 10,
            "estimated_time": "00:30:00"
        })
        self.assertEqual(response.status_code, 201)
        self.moto.refresh_from_db()
        self.assertFalse(self.moto.available)
