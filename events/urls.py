from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register_view, name='register'),
    path('contact/', views.contact_view, name='contact'),
    path('categories/', views.category_list, name='categories'),
    path('category/<slug:slug>/', views.event_list_by_category, name='event_list_by_category'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('search/', views.event_search, name='event_search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('favorites/', views.favorites, name='favorites')
]
