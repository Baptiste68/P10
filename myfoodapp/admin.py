from django.contrib import admin

from .models import Question, Food, Categories

# Register your models here.

admin.site.register(Question)
admin.site.register(Food)
admin.site.register(Categories)