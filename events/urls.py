from django.urls import path, include
from . import views

urlpatterns = [
    # path('event/create/', views.event_create, name='event_create'),
    # path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('contact/', views.contact_view, name='contact'),
    path('categories/', views.category_list, name='categories'),
    path('category/<slug:slug>/', views.event_list_by_category, name='event_list_by_category'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('search/', views.event_search, name='event_search'),
    path('logout/', views.logout_view, name='logout'),
    path('favorites/', views.favorites, name='favorites'),
    path('bookings/', include('bookings.urls')),
]
