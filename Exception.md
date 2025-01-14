## `Не находит board/advertisement_detail.html` 

1. Шаблон `advertisement_detail.html` находиться в функции `def advertisement_detail(request, pk):`
2. Функция `def advertisement_detail(request, pk):`вызывается через путь 
    `path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),`через `advertisement`
    из шаблона advertisement_list
3. 