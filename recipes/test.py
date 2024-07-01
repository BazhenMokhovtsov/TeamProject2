import re
from django.shortcuts import render, redirect

from .models import Recipe, RecipeIngredient, Ingredient
from .forms import RecipeForm,RecipeIngredientForm, IngredientForm



def recipe_handler(request, recipe_id):
    recipe = Recipe.objects.get(pk = recipe_id)
    ingredients_str = recipe.ingredients

    ingredients_list = [ing.strip() for ing in re.split(r'[, <p> : =]', ingredients_str) if ing.strip()]
    ingredients_quantity_list = [q.strip() for q in re.split(r'[a-z A-Z <p> , . = ]', ingredients_str) if q.strip()]
    print(ingredients_quantity_list)

    found_ingredients = []
    not_found_ingredients = []
    total_calories = 0
    total_cost = 0

    for item in ingredients_list:
        # Найти ингредиент и количество в каждом элементе
        match = re.search(r'(\D+)\s*(\d+)', item.strip())
        if match:
            ingredient_name = match.group(1).strip()
            quantity = match.group(2)

            try:
                ingredient = Ingredient.objects.get(name=ingredient_name.capitalize())
                found_ingredients.append(ingredient)

                # Вычисление калорий и стоимости
                calories = (ingredient.calories * quantity) / 100
                cost = (ingredient.price * quantity) / 100
                total_calories += calories
                total_cost += cost
            except Ingredient.DoesNotExist:
                not_found_ingredients.append(ingredient_name)
        else:
            not_found_ingredients.append(item.strip())

    return {
        'found_ingredients': found_ingredients,
        'not_found_ingredients': not_found_ingredients,
        'total_calories': total_calories,
        'total_cost': total_cost,
    }