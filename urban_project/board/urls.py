from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('edit_advertisement/<int:pk>/', views.AdvertisementUpdateView.as_view(), name='edit_advertisement'),
    path('advertisement/<int:ad_id>/delete/', views.delete_advertisement, name='delete_advertisement'),
    path('advertisement/<int:advertisement_id>/like/', views.like_def, name='like_def'),
    path('advertisement/<int:advertisement_id>/dislike/', views.dislike_def, name='dislike_def'),
]
