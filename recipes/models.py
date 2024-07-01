from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Ингредиент')
    calories = models.IntegerField(verbose_name="Каллории", null=True)
    price = models.FloatField(verbose_name="Цена", null=True)
    wight = models.IntegerField(verbose_name="Вес", null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class Recipe(models.Model):
    title = models.CharField(max_length=200,verbose_name='Название блюда')
    description = models.TextField(verbose_name='Описание')
    # ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
    ingredients = models.TextField(verbose_name='Ингредиенты', null=True)
    instructions = models.TextField(verbose_name='Инструкция')
    is_duty = models.BooleanField(verbose_name='Дежурное блюдо', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Блюдо добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Блюдо обновлено')
    image = models.ImageField(upload_to='recipes/%Y/%m/%d/', blank=True, null=True, verbose_name='Картинка к блюду')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updated_at']

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Ингредиенты для рецепта')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    quantity = models.IntegerField(verbose_name='Количество ингредиента')


    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.recipe.title}"


