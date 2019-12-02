import datetime
import json

from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.urls import reverse, path
from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Food, Categories, foodcate, saved
from .views import get_better_food, searching_cat, ProductView, connexion
from .views import creation, SavedView, AutoCompleteView, pwdchange
from .views import SearchView
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

    def test_pwd_change(self):
        log = self.client.login(username='basim', password='simba')
        self.client.force_login(self.user_1)
        user = User.objects.get(email="bas@bas.bas")
        req = self.client.post(reverse('myfoodapp:pwdchange'), {
            "old_password": "simba",
            "new_password": "sim",
            "new_password_b": "sim",
            'user': user
        })
        user = authenticate(username="basim", password="sim")
        self.assertTrue(user)

    def cleanUp(self):
        self.user_1.delete()


class FoodAndCatTest(TestCase):
    template_name = ''

    def test_better_food(self):
        initiate()
        create_food("banane", "1", "", "mystore", "None", "", "")
        id_food1 = Food.objects.only(
            'id').get(name_food="pomme").id
        self.assertEqual(get_better_food(
            "chocolat", "dessert")[0]['Food_id_id'], id_food1)

    def test_search_no_note(self):
        self.template_name = 'myfoodapp/search.html'
        factory = RequestFactory()
        initiate()
        create_food("banane", "1", "", "mystore", "None", "", "")
        self.assertEqual(get_better_food("banane", "dessert"), "Err")

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

    def test_autocomplet(self):
        create_food("Haricots Plats", 12, "", "", 'A', "", "")
        create_food("Haricots noirs", 1, "", "", 'A', "", "")
        create_food("Oeufs Plats", 2, "", "", 'A', "", "")
        self.template_name = 'myfoodapp/index.html'
        factory = RequestFactory()
        request = factory.get('/index/', {'term': 'hari'})
        response = AutoCompleteView.get(self, request)

        result = []

        for entry in response:
            my_json = entry.decode('utf8').replace("'", '"')
            value = json.loads(my_json)
            for data in value:
                result.append(data['value'])
        self.assertEqual(result, ['Haricots Plats', 'Haricots noirs'])
