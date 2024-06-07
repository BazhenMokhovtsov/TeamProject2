from django import forms
from .models import Recipe, Ingredient, RecipeIngredient
from django.forms import inlineformset_factory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'instructions', 'description','ingredients','is_duty', 'image', ]

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'calories', 'price']

class RecipeIngredientForm(forms.ModelForm):
    # ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), label='Выбор ингредиента')
    # recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(), label='Список рецептов')

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', ]

# RecipeIngredientFormSet = inlineformset_factory(
#     Recipe,
#     RecipeIngredient,
#     form=RecipeIngredientForm,
#     extra=1,
#     can_delete=True 
# )

