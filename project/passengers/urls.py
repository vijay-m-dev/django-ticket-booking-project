from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('book_ticket/<str:pk>', views.book_ticket, name="book_ticket"),
    path('delete_ticket/<str:pk>', views.delete_ticket, name="delete_ticket"),
    path('profile',views.profile, name="profile"),
    path('send_email/<str:pk>',views.success, name='send_email'),
]


