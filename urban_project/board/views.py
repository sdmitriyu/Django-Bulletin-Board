from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from board.models import Advertisement
from board.forms import AdvertisementForm
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

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