from django.shortcuts import render, redirect
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
    return render(request, 'home.html')

def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})

def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

@login_required
def add_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


class AdvertisementUpdateView(UpdateView):
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
