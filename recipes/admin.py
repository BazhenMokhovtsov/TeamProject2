from django.contrib import admin
from .models import *

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title']



@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe']
