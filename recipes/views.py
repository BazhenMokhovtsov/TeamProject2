from django.shortcuts import render, redirect

from .models import Recipe, RecipeIngredient, Ingredient
from .forms import RecipeForm,RecipeIngredientForm, IngredientForm


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

    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipes:add_ingredient')
    else:
        form = IngredientForm()

    context = {
        'form': form,
    }

    return render(request, 'recipes/add_ingredient.html', context)

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
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe_id = recipe_id)

    context = {
        'recipe': recipe,
        'ingredients': ingredients,
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
        
    
# def del_ingredient(request, ingredient_id):
#     ingredients = RecipeIngredient.objects.get(ingredient_id = ingredient_id)
#     ingredients.delete
#     return render(request, 'recipes:add_ingredient_to_recipe', ingredient_id = ingredients.ingredient_id)

def del_ingredient(request, recipe_id, ingredient_id):
    ingredient = RecipeIngredient.objects.filter(recipe_id=recipe_id, ingredient_id=ingredient_id)
    ingredient.delete()
    return redirect('recipes:single_recipe', recipe_id=recipe_id)


