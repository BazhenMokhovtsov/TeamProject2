import re
from django.shortcuts import render, redirect
import random
from django.views.decorators.http import require_http_methods

from .models import Recipe, RecipeIngredient, Ingredient
from .forms import RecipeForm,RecipeIngredientForm, IngredientForm

# Обрабатывает строку "ингредиенты" в моделе Рецепт и сравнивает ингредиенты с обьектами модели Ингредиент.
def recipe_handler(request, recipe_id):
    recipe = Recipe.objects.get(pk = recipe_id)
    ingredients_str = recipe.ingredients.capitalize()

    ingredients_list = [ing.strip() for ing in re.split(r'[,:&^/(a-z); :<p>=\-(\d+)]', ingredients_str) if ing.strip()]
    ingredients_quantity_list = re.findall(r'\d+(?:[\.]\d)?', ingredients_str)
    # print(ingredients_quantity_list)
    
    found_ingredients = []
    not_found_ingredients = []
    total_calories = 0
    total_cost = 0

    for ing in ingredients_list:
        try:
            ingredient = Ingredient.objects.get(name=ing.capitalize())
            found_ingredients.append(ingredient)
        except Ingredient.DoesNotExist:
            not_found_ingredients.append(ing)

    quantity_index = 0
    for ing in found_ingredients:
        if quantity_index < len(ingredients_quantity_list):
            quantity_str = ingredients_quantity_list[quantity_index]
            quantity = float(quantity_str)
            ing_info = Ingredient.objects.get(name=ing.name)
            calories = (ing_info.calories * quantity)
            cost = (ing_info.price / 1000 * ing_info.wight) * quantity
            total_calories += calories
            total_cost += round(cost, 2)
            quantity_index += 1
            print(f"Ингредиент: {ing}, Количество: {quantity} Цена: {cost} Калории: {calories} Калории за ед: {ing_info.wight}")

    return {
        'found_ingredients': found_ingredients,
        'not_found_ingredients': not_found_ingredients,
        'total_calories': total_calories,
        'total_cost': total_cost,
        
    }


def add_recipe(request):

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save()
            return redirect('recipes:add_ingredient_to_recipe', recipe_id=recipe.id) # Сохраняем айди сохраненного рецепта и передаем его
    else:
        recipe_form = RecipeForm()

    context = {
        'recipe_form': recipe_form,
    }

    return render(request, 'recipes/add_recipe.html', context)


def add_ingredient_to_recipe(request, recipe_id=None):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            recipe_ingredient = form.save(commit=False)
            recipe_ingredient.recipe = recipe    
            recipe_ingredient.save()
            return redirect('recipes:add_ingredient_to_recipe', recipe_id=recipe.id)
    else:
        form = RecipeIngredientForm()

    context = {
        'form': form,
        'ingredients': ingredients,
        'recipe': recipe,
    }
    
    return render(request, 'recipes/add_ingredient_to_recipe.html', context)


def add_ingredient(request):
    all_ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipes:add_ingredient')
    else:
        form = IngredientForm()

    context = {
        'form': form,
        'all_ingredients':all_ingredients,
    }

    return render(request, 'recipes/add_ingredient.html', context)


def edit_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get( id=ingredient_id)

    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('recipes:add_ingredient')
    else:
        form = IngredientForm(instance=ingredient)

    context = {
        'form': form,
        'ingredient': ingredient,
    }

    return render(request, 'recipes/edit_ingredient.html', context)


def show_all_recipes(request):
    recipes = Recipe.objects.all()
    
    context = {
        'recipes': recipes,
    }

    return render(request, "recipes/all_recipes.html", context)


def show_duty_recipes(request):
    duty_recipe = Recipe.objects.filter(is_duty=True)

    context = {
        'duty_recipe': duty_recipe,
    }

    return render(request, 'recipes/duty_recipe.html', context)


def single_recipe(request, recipe_id):
    ing_info = recipe_handler(request, recipe_id)

    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe_id = recipe_id)


    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'found_ingredients': ing_info['found_ingredients'],
        'not_found_ingredients': ing_info['not_found_ingredients'],
        'total_calories': ing_info['total_calories'],
        'total_cost': ing_info['total_cost'],
    }

    return render(request, 'recipes/single_recipe.html', context)


def edit_recipe(request, recipe_id):
    recipe_to_edit = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe_to_edit)
        if form.is_valid():
            form.save()
            return redirect('recipes:add_ingredient_to_recipe', recipe_id=recipe_to_edit.id)
    else:
        form = RecipeForm(instance=recipe_to_edit)

    context = {
        'form': form,
    }
    
    return render(request, 'recipes/edit_recipe.html', context)


def del_ingredient(request, recipe_id, ingredient_id):
    ingredient = RecipeIngredient.objects.filter(recipe_id=recipe_id, ingredient_id=ingredient_id)
    ingredient.delete()
    return redirect('recipes:single_recipe', recipe_id=recipe_id)


def week_recipe(request):
    # db_path = 'db.sqlite3'
    # table_name = 'recipes_recipe'
    num_recipes = 3
    sessions_key = 'random_recipes_index'
    week_recipes_index = request.session.get(sessions_key)
    
    # Получаем случайные номера рецептов и записываем их в сессии.
    if not week_recipes_index:
        total_rows = Recipe.objects.filter(is_duty=True).count()
        week_recipes_index = random.sample(range(total_rows), min(num_recipes, total_rows)) # min необходимо, чтобы не запрашивать больше рецептов, чем есть всего строк в таблице.
        # sample - получаем уникальные значения в диапозоне.
        request.session[sessions_key] = week_recipes_index

    # connect_bd = sqlite3.connect(db_path)
    # cursor = connect_bd.cursor()
    # cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    # total_rows = cursor.fetchone()[0]
    # connect_bd.close()

    # random_recipes = [Recipe.objects.all()[i] for i in week_recipes_index]

    random_recipes = []
    for recipe in week_recipes_index:
        random_recipe = Recipe.objects.filter(is_duty=True)[recipe]
        random_recipes.append(random_recipe)

    context = {
        "random_recipes": random_recipes,
    }

    return render(request, 'recipes/week.html', context)

# Функция обновления списка рецептов на неделю.
def regenerate_recipes(request):
    sessions_key = 'random_recipes_index'
    if sessions_key in request.session:
        del request.session[sessions_key]
    return redirect('recipes:week_recipe')