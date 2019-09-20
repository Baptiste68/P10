import datetime

from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.urls import reverse, path
from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Food, Categories, foodcate, saved
from .views import get_better_food, searching_cat, ProductView, connexion
from .views import creation, SavedView
from . import views
from . import forms


def create_food(name, qty, danger, store, score, link, img):
    return Food.objects.create(name_food=name, quantity_food=qty,
                               dangers_food=danger,
                               store_food=store, nutri_score_food=score,
                               link_food=link, img_food=img)


def create_category(name):
    return Categories.objects.create(name_categories=name)


def create_foodcate(food_id, cate_id):
    return foodcate.objects.create(Food_id=food_id, Categories_id=cate_id)


def initiate():
    create_food("pomme", "1", "", "mystore", "A", "", "")
    create_food("chocolat", "100g", "", "mystore", "C", "", "")
    create_category("dessert")
    id_category = Categories.objects.only(
        'id').get(name_categories="dessert").id
    id_food1 = Food.objects.only(
        'id').get(name_food="pomme").id
    id_food2 = Food.objects.only(
        'id').get(name_food="chocolat").id
    create_foodcate(Food.objects.get(id=id_food1),
                    Categories.objects.get(id=id_category))
    create_foodcate(Food.objects.get(id=id_food2),
                    Categories.objects.get(id=id_category))


class GeneralTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse('myfoodapp:index'))
        self.assertEqual(response.status_code, 200)

    def test_legals(self):
        response = self.client.get(reverse('myfoodapp:legals'))
        self.assertEqual(response.status_code, 200)

    def test_creationsuccess(self):
        response = self.client.get(reverse('myfoodapp:creationsuccess'))
        self.assertEqual(response.status_code, 200)


class UserTest(TestCase):
    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create_user(
            'basim', 'bas@bas.bas', 'simba', first_name='first_name',
            last_name='last_name')

    template_name = ''

    def test_create_usr(self):
        factory = RequestFactory()
        request = factory.post("creation/", {
            "first_name": "Bas",
            "last_name": "Im",
            "email": "bas@im.com",
            "password": "simba",
            "username": "basim2"})
        response = creation(request)
        user = User.objects.get(email="bas@im.com")
        self.assertEqual(user.username, "basim2")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = authenticate(username="basim", password="simba")
        self.assertTrue(user)

    def test_save_food(self):
        initiate()
        id_food1 = Food.objects.only(
            'id').get(name_food="pomme").id
        id_food2 = Food.objects.only(
            'id').get(name_food="chocolat").id
        log = self.client.login(username='basim', password='simba')
        self.client.force_login(self.user_1)
        user = User.objects.get(email="bas@bas.bas")
        response = self.client.get(reverse('myfoodapp:saved'), {
            'sub': id_food1,
            'tosub': id_food2,
            'user': user
        })
        self.assertEqual(response.status_code, 200)

    def cleanUp(self):
        self.user_1.delete()


class FoodAndCatTest(TestCase):
    template_name = ''

    def test_better_food(self):
        initiate()
        id_food1 = Food.objects.only(
            'id').get(name_food="pomme").id
        self.assertEqual(get_better_food(
            "chocolat", "dessert")[0]['Food_id_id'], id_food1)

    def test_searching_cat(self):
        initiate()
        self.assertEqual(searching_cat("pomme"), "dessert")

    def test_search_view(self):
        self.template_name = 'myfoodapp/search.html'
        initiate()
        id_food1 = Food.objects.only(
            'id').get(name_food="pomme").id
        factory = RequestFactory()
        request = factory.get('/search/', {'product': id_food1})
        result = ProductView.get(self, request)
        self.assertEqual(result.status_code, 200)

    def test_product_view(self):
        self.template_name = 'myfoodapp/product.html'
        initiate()
        id_food1 = Food.objects.only(
            'id').get(name_food="pomme").id
        factory = RequestFactory()
        request = factory.get('/product/', {'product': id_food1})
        result = ProductView.get(self, request)
        self.assertEqual(result.status_code, 200)
