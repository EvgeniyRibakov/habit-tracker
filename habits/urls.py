from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    HabitListCreateView,
    PublicHabitListView,
    HabitDetailView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/public/', PublicHabitListView.as_view(), name='public-habit-list'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
]
