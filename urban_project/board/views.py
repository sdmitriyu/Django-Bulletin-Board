from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from board.models import Advertisement, Like, Dislike
from board.forms import AdvertisementForm
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return redirect('home')



def signup(request):
    '''
    Функция регистрации новых пользователей
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    '''
    Направляет на домашнюю страницу
    :param request:
    :return:
    '''
    return render(request, 'home.html')

def advertisement_list(request):
    '''
    Функция вызывает список объявлений из базы данных
    :param request:
    :return:
    '''
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})

def advertisement_detail(request, pk):
    '''
    Функция показывает детали объявления
    :param request:
    :param pk:
    :return:
    '''
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

@login_required
def add_advertisement(request):
    '''
    Функция создаёт новое объявление. Так же проверяет, зарегистрирован ли пользователь, подающий объявление
    :param request:
    :return:
    '''
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})

def handle_uploaded_file(f):
    with open("media/" + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)



class AdvertisementUpdateView(UpdateView):
    '''
    Встроенный в Django класс для редактирования объявлений
    '''
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/edit_advertisement.html'
    context_object_name = 'advertisement'

    def form_valid(self, form):
        # Дополнительная логика, до сохранения формы, если необходимо
        return super().form_valid(form)

    def get_success_url(self):
        # Возвращает URL адрес для перенаправления пользователя после успешного редактирования
        return reverse('board:advertisement_detail', kwargs={'pk': self.object.pk})



def delete_advertisement(request, ad_id):
    '''
    Функция удаления объявлений
    :param request:
    :param ad_id:
    :return:
    '''
    advertisement = get_object_or_404(Advertisement, id=ad_id)

    if request.method == 'POST':
        advertisement.delete()
        return redirect('board:advertisement_list')

    return render(request, 'board/delete_advertisement.html', {'advertisement':advertisement})


from django.shortcuts import get_object_or_404, redirect, render
from .models import Advertisement, Like, Dislike


def like_def(request, advertisement_id):
    """
    Считает отдельно количество лайков от зарегистрированных пользователей и от гостей
    :param request:
    :param advertisement_id:
    :return:
    """
    advertisement = get_object_or_404(Advertisement, id=advertisement_id)

    # Для аутентифицированных пользователей
    if request.user.is_authenticated:
        # Проверяем, ставил ли пользователь лайк
        if Like.objects.filter(user=request.user, advertisement=advertisement).exists():
            # Если лайк уже существует, ничего не делаем
            return render(
                request,
                'board/advertisement_detail.html',
                {'advertisement': advertisement, 'total_likes': advertisement.total_likes()}
            )

        # Удаляем дизлайк, если он существует от этого пользователя
        Dislike.objects.filter(user=request.user, advertisement=advertisement).delete()
        # Если лайка нет, создаём новый
        Like.objects.create(user=request.user, advertisement=advertisement)

    # Для гостей
    else:
        user_has_liked = request.session.get(f'has_liked_{advertisement_id}', False)
        user_has_disliked = request.session.get(f'has_disliked_{advertisement_id}', False)

        if user_has_liked:
            # Если лайк уже проставлен, ничего не делаем
            return render(
                request,
                'board/advertisement_detail.html',
                {'advertisement': advertisement, 'total_likes': advertisement.total_likes()}
            )

        # Заменяем дизлайк на лайк
        if user_has_disliked:
            request.session[f'has_disliked_{advertisement_id}'] = False

        # Помечаем, что лайк был поставлен
        request.session[f'has_liked_{advertisement_id}'] = True

    advertisement.refresh_from_db()  # Обновляем данные объявления
    return render(
        request,
        'board/advertisement_detail.html',
        {'advertisement': advertisement, 'total_likes': advertisement.total_likes()}
    )



def dislike_def(request, advertisement_id):
    """
    Считает количество дизлайков отдельно от зарегистрированных пользователей, и отдельно от гостей
    :param request:
    :param advertisement_id:
    :return:
    """
    advertisement = get_object_or_404(Advertisement.total_dislikes(), id=advertisement_id)

    # Для аутентифицированных пользователей
    if request.user.is_authenticated:
        # Проверяем, ставил ли пользователь дизлайк
        if Dislike.objects.filter(user=request.user, advertisement=advertisement.total_dislikes()).exists():
            # Если дизлайк уже существует, ничего не делаем
            return render(
                request,
                'board/advertisement_detail.html',
                {'advertisement': advertisement, 'total_dislikes': advertisement.total_dislikes()}
            )

        # Удаляем лайк, если он существует от этого пользователя
        Like.objects.filter(user=request.user, advertisement=advertisement.total_likes()).delete()
        # Если дизлайка нет, создаём новый
        Dislike.objects.create(user=request.user, advertisement=advertisement.total_dislikes())

    # Для гостей
    else:
        user_has_disliked = request.session.get(f'has_disliked_{advertisement_id}', False)
        user_has_liked = request.session.get(f'has_liked_{advertisement_id}', False)

        if user_has_disliked:
            # Если дизлайк уже проставлен, ничего не делаем
            return render(
                request,
                'board/advertisement_detail.html',
                {'advertisement': advertisement, 'total_dislikes': advertisement.total_dislikes()}
            )

        # Заменяем лайк на дизлайк
        if user_has_liked:
            request.session[f'has_liked_{advertisement_id}'] = False

        # Помечаем, что дизлайк был поставлен
        request.session[f'has_disliked_{advertisement_id}'] = True

    advertisement.refresh_from_db()  # Обновляем данные объявления
    return render(
        request,
        'board/advertisement_detail.html',
        {'advertisement': advertisement, 'total_dislikes': advertisement.total_dislikes()}
    )


@receiver(post_save, sender=Advertisement)
def update_ad_count_on_create(sender, instance, created, **kwargs):
    """
    Увеличивает счётчик оъявлений у связанного профильного пользователя
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        profile = instance.user.profile
        profile.ad_count += 1
        profile.save()

@receiver(post_delete, sender=Advertisement)
def update_ad_count_on_delete(sender, instance, **kwargs):
    """
    Уеньшает счётчик оъявлений у связанного профильного пользователя, если счётчик больше нуля
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    profile = instance.user.profile
    if profile.ad_count > 0:
        profile.ad_count -= 1
        profile.save()

@receiver(post_save, sender=Advertisement)
def update_like_dislike_count(sender, instance, created, **kwargs):
    """
    Увеличивает количество лайков или дизлайков в профиле пользователя и в объявлении.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        advertisement = instance.advertisement
        profile = advertisement.user.profile
        if instance.is_like:
            profile.like_count += 1
            advertisement.total_likes += 1
        else:
            profile.dislike_count += 1
            advertisement.total_dislikes += 1
        profile.save()
        advertisement.save()

@receiver(post_delete, sender=Advertisement)
def update_like_dislike_count_on_delete(sender, instance, **kwargs):
    """
     Уменьшает количество лайков или дизлайков в профиле пользователя и в объявлении, если они больше нуля.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    advertisement = instance.advertisement
    profile = advertisement.user.profile
    if instance.is_like and profile.like_count > 0:
        profile.like_count -= 1
        advertisement.total_likes -= 1
    elif not instance.is_like and profile.dislike_count > 0:
        profile.dislike_count -= 1
        advertisement.total_dislikes -= 1
    profile.save()
    advertisement.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Если пользователь только что создан, функция создает связанный объект профиль.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Profile.objects.create(user=instance)


@csrf_exempt
@require_POST
def like_advertisement(request, advertisement_id):
    """
     Используя `get_or_create`, добавляет лайк к указанному объявлению от текущего пользователя.
     Удаляет дизлайк, если он ранее существовал.
    :param request:
    :param advertisement_id:
    :return:
    """
    advertisement = get_object_or_404(Advertisement, id=advertisement_id)
    user = request.user
    Like.objects.get_or_create(user=user, advertisement=advertisement)
    Dislike.objects.filter(user=user, advertisement=advertisement).delete()  # Удаляем дизлайк, если он был
    response = {
        'likes_count': advertisement.total_likes(),
        'dislikes_count': advertisement.total_dislikes()
    }
    return JsonResponse(response)

@csrf_exempt
@require_POST
def dislike_advertisement(request, advertisement_id):
    """
    Используя `get_or_create`, добавляет дизлайк к указанному объявлению от текущего пользователя.
    Удаляет лайк, если он ранее существовал.
    :param request:
    :param advertisement_id:
    :return:
    """
    advertisement = get_object_or_404(Advertisement, id=advertisement_id)
    user = request.user
    Dislike.objects.get_or_create(user=user, advertisement=advertisement)
    Like.objects.filter(user=user, advertisement=advertisement).delete()  # Удаляем лайк, если он был
    response = {
        'likes_count': advertisement.total_likes(),
        'dislikes_count': advertisement.total_dislikes()
    }
    return JsonResponse(response)