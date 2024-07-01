Описание проекта.

    Создаем вебприложение которое будет:
        1. Записывать рецепты понравившихся блюд.
        2. Помогать с выбором держурных блюд на неделю. Все имеющиеся рецепты с пометкой (деружное) методом рандом. 
        3. Составлять список продуктов для недельного меню. (цена опционально)
        4. Вести подсчёт стоимости и каллорийности блюда
        5. Помогать выбрать блюдо исходя из имеющихся продуктов.


Что для этого нужно:

    Модели
        Рецепт
            Название блюда(Заголовк)+
            Ингредиенты+
            Количество нужного ингредиента.+
            Инструкция+
            Держурное блюдо+
            дата добавления+
            слаг+
            время приготовления

        Ингредиенты(Продукты)
            Название
            цена

        Блюда недели
            Дата создания
            рецепт
        


Description of the project.

    We create a web application that will be:
        1. Record recipes for your favorite dishes.
        2. Help with the choice of holding dishes for a week. All available recipes marked (fingering) by random.    
        3. Make a list of products for a weekly menu.
        4. Count the cost and calorie content of the dish
        5. Help choose a dish based on the available products.


 What is needed for this:

    Models
        Recipe
            title
            description
            ingredients
            instructions
            created_at
            updated_at
            image

        Ingredients (products)
            name
            calories
            price
            wight

