from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.show_all_recipes, name='show_all_recipes'),
    path('duty_recipes/', views.show_duty_recipes, name='show_duty_recipes'),
    path('singe_recipe/<int:recipe_id>', views.single_recipe, name = 'single_recipe'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('add_ingredient_to_recipe/<int:recipe_id>', views.add_ingredient_to_recipe, name='add_ingredient_to_recipe'),
    path('edit_recipe/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('delete_ingredient/<int:recipe_id>/<int:ingredient_id>/', views.del_ingredient, name='del_ingredient'),
    path('edit-ingredient/<int:ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    # path('edit_ing/<int:ingredient_id>/', views.edit_ing, name='edit_ing'),
    path('week/', views.week_recipe, name= 'week_recipe'),
    path('regenerate/', views.regenerate_recipes, name='regenerate_recipes')
]