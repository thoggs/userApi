from django.urls import path

from api.views import index

urlpatterns = [
    path('users', index, name='users'),
    path('users/<int:user_id>', index, name='user-detail'),
]
