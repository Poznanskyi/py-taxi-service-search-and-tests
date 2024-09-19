from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Driver, Car, Manufacturer
from .forms import DriverCreationForm


DEFAULT_USER_PARAMS = {
    "username": "test",
    "password": "test123",
    "first_name": "Brad",
    "last_name": "Pitt",
    "license_number": "ABC12345",
}


class TestDriverCreation(TestCase):
    def setUp(self):
        self.base_driver = {
            "username": "test",
            "password": "3231qwerty",
        }

    def test_create_driver(self):
        self.assertEqual(Driver.objects.count(), 0)
        form = DriverCreationForm(self.base_driver)
        self.assertTrue(form.is_valid())

    def test_correct_license_number(self):
        self.base_driver["license_number"] = "ABC12345"
        form = DriverCreationForm(self.base_driver)
        self.assertTrue(form.is_valid())

    def test_incorrect_license_number(self):
        self.base_driver["license_number"] = "ABC12345"
        form = DriverCreationForm(self.base_driver)
        self.assertFalse(form.is_valid())


class TestManufacturer(TestCase):
    def test_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(str(manufacturer), "AUDI" "Germany")


class TestCarModel(TestCase):
    def test_str(self):
        model = "Test"
        manufacturer = Manufacturer.objects.create(
            name="Test", country="land"
        )
        car = Car.objects.create(model=model, manufacturer=manufacturer)
        self.assertEqual(str(car), model)


class TestDriverModel(TestCase):
    def test_str(self):
        driver = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.assertEqual(
            str(driver),
            "{username} ({first_name} {last_name})".format(
                **DEFAULT_USER_PARAMS
            ),
        )


class PublicTestIndex(TestCase):
    def test_login_required(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PublicTestManufacturerList(TestCase):
    def test_login_required(self):
        url = reverse("taxi:manufacturer_list")
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)


class PublicTestCarList(TestCase):
    def test_login_required(self):
        url = reverse("taxi:car_list")
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)


class PublicTestDriverList(TestCase):
    def test_login_required(self):
        url = reverse("taxi:driver_list")
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)


class PrivateTestIndex(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_counter_of_visits(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response, "the first time")
        self.assertEqual(response, "the second time")
        self.assertEqual(response, "the third time")


class PrivateTestManufacturerList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_search(self):
        name = "QWERTY"
        country = "Neverland"
        Manufacturer.objects.create(name=name, country=country)
        url = reverse("taxi:manufacturer_list")
        response = self.client.get(url, {"name": name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response, name)


class PrivateTestCarList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_search(self):
        model = "QWERTY"
        country = "Neverland"
        manufacturer = Manufacturer.objects.create(
            model=model,
            country=country
        )
        Car.objects.create(model=model, manufacturer=manufacturer)
        url = reverse("taxi:car_list")
        response = self.client.get(url, {"model": model})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, model)


class PrivateTestDriverList(TestCase):
    def setUp(self):
        self.username = DEFAULT_USER_PARAMS["username"]
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_search(self):
        url = reverse("taxi:driver_list")
        response = self.client.get(url, {"username": self.username})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{self.username}")
