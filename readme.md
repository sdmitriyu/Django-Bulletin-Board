# Доска обьявлений на Django
**Данный проект реализует доску объявлений на фре
йворке Dlango,
который реализует механизмы регистрации, показа списка объявлений 
до регистрации и после,**
---
## |[urban_progect / urls.py](urban_project%2Furban_project%2Furls.py)
Корневой url аспределитель маршрутов
- `path('admin/', admin.site.urls)` - ведёт на административную страницу веб-сайта на Django
- `path('board/', include('board.urls', namespace='board'))` - Перенаправление к модулю URL в приложении board
- `path('accounts/logout/', board_views.logout_view, name='logout')` - Переход к функции logout_view
- `path('accounts/', include('django.contrib.auth.urls'))` - Стандартная форма аунтификации Django
- `path('', board_views.home, name='home')` - Переход к главной страница сайта

---
## |[urls.py](urban_project%2Fboard%2Furls.py)
Распределитель маршрутов в пртложении board
- `app_name = 'board'` - Пространство имён для организации маршрутов в приложении
- `path('', views.advertisement_list, name='advertisement_list')`- Переносит на страницу объявлений
- `path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail')`- Переносит на 
страницу с показом деталей объявления.
- `path('add/', views.add_advertisement, name='add_advertisement')`- Переносит на страницу создания объявлений
---
## |[views.py](urban_project%2Fboard%2Fviews.py)

### _def logout_view(request):_
Функция разлогинивание на сайте.
- Вызывает функцию разлогинивания
- перенаправляет на страницу home

### _def signup(request):_
Функция регистрирует пользователя на сайте.
- Принимает информацию с формы `SignUpForm`
- Поизводит её вылидацию
- В случае успешной валидации:
  - Сохраняет её в переменную user
  - Сохраняет во встроенную функцию user
  - перекидывает в URL приложения
- При неудачной валидации:
  - Перенаправляет на страницу формы входа `signup.html`
![signup.png](urban_project%2FImages%2Fsignup.png)

### _def home(request):_
Функция перекидывает на страницу `home.html`
![home.png](urban_project%2FImages%2Fhome.png)

### _def advertisement_list(request):_
Функция достаёт из базы данных все оъявления, и передаёт на 
страницу `board/advertisement_list.html`
![advertisement_list.png](urban_project%2FImages%2Fadvertisement_list.png)

### _def advertisement_detail(request, pk):_
Функция для отображения деталей объявления.
- Достаёт детали оъявления из базы данных и сохраняет в переменную advertisement
- передаёт в шаблон `advertisement_detail.html`
![advertisement_detail.png](urban_project%2FImages%2Fadvertisement_detail.png)

### _def add_advertisement(request):_
Форма для сохранения нового оъявления с изображением
- Принимает форму объявления
- Проверяет его валидность
- если валидность подтверждена
  - Сохраняются данные формы без сохранения в базу данных
  - При помощи декоратора, есть ли автор объявления в базе
  - объявление сохраняется
  - Пользователя перекидывает на страницу `advertisement_list`
- Если валидность не подтверждена
  - Возвращается форма заполнения объявления
![add_advertisement.png](urban_project%2FImages%2Fadd_advertisement.png)

### 1. AdvertisementUpdateView — класс для редактирования объявлений

Класс основан на встроенной в Django представлении UpdateView. Он позволяет пользователю редактировать объявление, предоставленное в форме.

#### Ключевые параметры:

- model: Модель, используемая для работы (Advertisement).
- form_class: Ссылка на форму, которая используется для представления данных (AdvertisementForm).
- template_name: Путь к HTML-шаблону, который будет отображать форму редактирования (board/edit_advertisement.html).
- context_object_name: Ключ доступа к объекту в контексте шаблона (advertisement).

#### Методы:

def form_valid(self, form):
    # Дополнительная логика обработки формы перед сохранением,
    # если это требуется
    return super().form_valid(form)

- Этот метод вызывается при успешной валидации формы. Можно добавить кастомную обработку данных объявлений до сохранения.

def get_success_url(self):
    # URL для перенаправления пользователя после успешного редактирования
    return reverse('board:advertisement_detail', kwargs={'pk': self.object.pk})

- Метод возвращает URL, на который будет перенаправлен пользователь после успешного сохранения изменений. В данном случае, это страница с подробной информацией о редактируемом объявлении.
![AdvertisementUpdateView.png](urban_project%2FImages%2FAdvertisementUpdateView.png)
---

### 2. delete_advertisement — функция удаления объявлений

Функция позволяет пользователям удалять свои объявления. Она требует подтверждения удаления, которое обрабатывается через POST-запрос.

#### Параметры:
- request: Передаёт данные запроса пользователя.
- ad_id: ID удаляемого объявления.

#### Логика работы:
1. Функция ищет объявление с указанным идентификатором (ad_id) через функцию get_object_or_404.
2. Если запрос — POST (подтверждение удаления), объявление удаляется с помощью метода delete.
3. После успешного удаления пользователь перенаправляется на список всех объявлений (board:advertisement_list).
4. В случае GET-запроса пользователю отображается страница подтверждения (board/delete_advertisement.html).

#### Код функции:

def delete_advertisement(request, ad_id):
    """
    Удаление объявления
    :param request: объект запроса
    :param ad_id: ID удаляемого объявления
    :return: HTTP ответ
    """
    advertisement = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        advertisement.delete()
        return redirect('board:advertisement_list')
    return render(request, 'board/delete_advertisement.html', {'advertisement': advertisement})"""
![delete_advertisement1.png](urban_project%2FImages%2Fdelete_advertisement1.png)
![delete_advertisement2.png](urban_project%2FImages%2Fdelete_advertisement2.png)
---
#### like_def(request, advertisement_id)

Функция для постановки лайка к объявлению. Лайк можно поставить как аутентифицированным пользователям, так и гостям.

- Параметры:
  - request: HTTP-запрос.
  - advertisement_id: ID объявления, к которому ставится лайк.

- Описание:
  - Проверяется, является ли пользователь аутентифицированным.
  - Если пользователь аутентифицирован, проверяется, поставил ли он лайк. Если лайк уже существует, ничего не происходит.
  - Для гостей используется сессия для хранения состояния лайка.
  - В обоих случаях увеличивается количество лайков у объявления.
  - После выполнения действия происходит редирект на страницу с деталями объявления.

#### dislike_def(request, advertisement_id)

Функция для постановки дизлайка к объявлению. Дизлайк можно поставить как аутентифицированным пользователям, так и гостям.

- Параметры:
  - request: HTTP-запрос.
  - advertisement_id: ID объявления, к которому ставится дизлайк.

- Описание:
  - Проверяется, является ли пользователь аутентифицированным.
  - Если пользователь аутентифицирован, проверяется, поставил ли он дизлайк. Если дизлайк уже существует, ничего не происходит.
  - Для гостей используется сессия для хранения состояния дизлайка.
  - В обоих случаях увеличивается количество дизлайков у объявления.
  - После выполнения действия происходит редирект на страницу с деталями объявления.
![Like and Dislike.png](urban_project%2FImages%2FLike%20and%20Dislike.png
---
#### `def update_ad_count_on_create(sender, instance, created, **kwargs):`
- **Описание**: Обработчик сигналов Django, вызываемый после создания объявления.
- **Назначение**: Увеличивает счетчик объявлений у профиля пользователя, к которому привязано объявление.

#### `def update_ad_count_on_delete(sender, instance, **kwargs):`   
- **Описание**: Обработчик сигналов Django, вызываемый после удаления объявления.
- **Назначение**: Уменьшает счетчик объявлений у профиля пользователя, если текущий счетчик больше нуля.

#### `def update_like_dislike_count(sender, instance, created, **kwargs):`   
- **Описание**: Обработчик сигналов Django, вызываемый после создания объекта, связанного с объявлением.
- **Назначение**: Увеличивает количество лайков или дизлайков в профиле пользователя и в объявлении при добавлении
нового лайка или дизлайка.

#### `def update_like_dislike_count_on_delete(sender, instance, **kwargs):`   
- **Описание**: Обработчик сигналов Django, вызываемый после удаления объекта, связанного с объявлением.
- **Назначение**: Уменьшает количество лайков или дизлайков в профиле пользователя и в объявлении, если они больше нуля.

#### `def create_user_profile(sender, instance, created, **kwargs):`   
- **Описание**: Обработчик сигналов Django, вызываемый после создания нового пользователя.
- **Назначение**: Создает новый профиль для пользователя сразу после его регистрации.

#### `def like_advertisement(request, advertisement_id):`   
- **Описание**: Вьюха Django, принимающая POST-запросы для добавления лайка к указанному объявлению.
- **Назначение**: Добавляет лайк от текущего пользователя и удаляет существующий дизлайк. Возвращает актуальные 
количество лайков и дизлайков в формате JSON.

#### `def dislike_advertisement(request, advertisement_id):`   
- **Описание**: Вьюха Django, принимающая POST-запросы для добавления дизлайка к указанному объявлению.
- **Назначение**: Добавляет дизлайк от текущего пользователя и удаляет существующий лайк. Возвращает актуальные
количество лайков и дизлайков в формате JSON.

---
## |[models.py](urban_project%2Fboard%2Fmodels.py)
Этот код представляет собой реализацию базовой модели объявлений и комментариев в Django, с использованием встроенного 
механизма ORM. Разделен на две модели: Advertisement (объявления) и Comment (комментарии). Каждый комментарий связан с 
определённым объявлением, а также с автором.

### Модель Advertisement

Модель представляет данные объявления.

#### Поля:

1. title  
   - Тип: CharField.  
   - Описание: Заголовок объявления.  
   - Ограничение: Максимальная длина строки - 255 символов.  

2. content  
   - Тип: TextField.  
   - Описание: Основное текстовое содержание объявления.  
   - Хранит длинные текстовые данные.  

3. author  
   - Тип: ForeignKey.  
   - Описание: Связь с моделью пользователя (User), который создал объявление.
   - Особенность:  
     - При удалении пользователя все его объявления будут удалены (on_delete=models.CASCADE).

4. created_at  
   - Тип: DateTimeField.  
   - Описание: Автоматически сохраняет дату и время создания объявления.  
   - Особенности:  
     - Устанавливается только один раз при создании (auto_now_add=True).

- str(self)
  - Описание: Возвращает название объявления (значение поля title) при попытке вывести объект в текстовом формате.

### Модель Comment

Модель представляет данные комментария к объявлению.

#### Поля:

1. advertisement  
   - Тип: ForeignKey.  
   - Описание: Связь с моделью Advertisement. Указывает, к какому объявлению относится комментарий.  
   - Особенности:  
     - При удалении объявления все связанные комментарии также удаляются (on_delete=models.CASCADE).  
     - Дополнительный параметр related_name='comments' позволяет удобно обращаться к комментариям объявления через 
обратную связь.

2. author  
   - Тип: ForeignKey.  
   - Описание: Связь с пользователем (User), который оставил комментарий.  
   - Особенности:  
     - При удалении пользователя все его комментарии будут удалены (on_delete=models.CASCADE).

3. content  
   - Тип: TextField.  
   - Описание: Содержимое комментария.

4. created_at  
   - Тип: DateTimeField.  
   - Описание: Автоматически сохраняет дату и время создания комментария.  
   - Особенности:  
     - Устанавливается только один раз при создании (auto_now_add=True).

- str(self)  
  - Описание: Возвращает текстовое описание комментария в формате: "Comment by {author} on {advertisement}".  
---

## |[forms.py](urban_project%2Fboard%2Fforms.py)

Этот код представляет собой набор Django-форм, предназначенных для работы с пользовательским вводом, а также для 
облегчения операций с моделью Advertisement. Код содержит:

1. Форма для взаимодействия с моделью Advertisement.
2. Форма для регистрации новых пользователей с использованием встроенной модели User.

В документации детализировано описание функциональности каждой формы, их структуры и назначения.

---

### AdvertisementForm

#### Назначение
Форма предназначена для:
- Создания и сохранения новых объявлений в базе данных.
- Редактирования полей существующих объектов модели Advertisement.

#### Особенности
- Наследуется от forms.ModelForm (Django автоматически генерирует форму, основываясь на переданной модели).
- Связана с моделью Advertisement, что избавляет от необходимости вручную определять поля в форме.

#### Класс Meta
- model: Определяет, с какой моделью будет работать форма. В данном случае, это модель Advertisement.
  
- fields: Список полей модели Advertisement, которые будут включены в форму:
  - title: Поле для указания заголовка объявления (например, текстовое описание названия).
  - content: Поле для текста объявления.
  - author: Поле, представляющее автора объявления (связывается с пользователем).

### SignUpForm

#### Назначение
Форма предназначена для регистрации новых пользователей. Используется в тех случаях, когда нужно предоставить простую и безопасную процедуру создания учетной записи.

#### Особенности
- Наследуется от UserCreationForm, что упрощает создание формы регистрации.
- Включает встроенную проверку пароля (два поля для пароля), чтобы убедиться, что данные введены корректно.
- Связана с моделью User (стандартной моделью для пользователей в Django).

#### Класс Meta
- model: Указывает, что форма работает с моделью User.
  
- fields: Список полей, которые пользователь сможет заполнить при регистрации:
  - username: Имя пользователя (уникальный идентификатор).
  - password1: Первый ввод пароля.
  - password2: Повторный ввод пароля для проверки совпадения.