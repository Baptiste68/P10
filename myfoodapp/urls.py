from django.urls import path

from . import views

app_name = 'myfoodapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('creation/', views.creation, name='creation'),
    path('compte/', views.CompteView.as_view(), name='compte'),
    path('populate/', views.PopulateView.as_view(), name='populate'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('saved/', views.SavedView.as_view(), name='saved'),
    path('viewsaved/', views.MyFoodView.as_view(), name='viewsaved'),
    path('details/', views.DetailsView.as_view(), name='details'),
    path('creationsuccess/', views.creation, name='creationsuccess'),
    path('my_view', views.ProductView.as_view(), name='my_view'),
    path('legals/', views.legals, name='legals'),
    path('failsearch/', views.failsearch, name='failsearch'),
]