from django.contrib import admin

from .models import Food, Categories
#from .forms import SearchForm

# Register your models here.

admin.site.register(Food)
admin.site.register(Categories)
#admin.site.register(SearchForm)
