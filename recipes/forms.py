from django import forms
# from django.forms import forms, Textarea
from tinymce.widgets import TinyMCE
from ckeditor.widgets import CKEditorWidget

from .models import Recipe, Ingredient, RecipeIngredient





class RecipeForm(forms.ModelForm):
    instructions = forms.CharField(widget=CKEditorWidget(), label='Инструкция')
    description = forms.CharField(widget=CKEditorWidget(), label='Описание')
    ingredients = forms.CharField(widget=CKEditorWidget(), label='Ингредиенты')
    

    class Meta:
        model = Recipe
        fields = ['title', 'instructions', 'description','ingredients','is_duty', 'image', ]
        # fields = ['title', 'instructions', 'description','ingredients','is_duty', 'image', ]

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'calories', 'price', 'wight']

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

