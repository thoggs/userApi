from rest_framework import routers

from api.views import UserViewSet, ObtainTokenViewSet


class ApiRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'users', UserViewSet, basename='users')
        self.register(r'token', ObtainTokenViewSet, basename='obtain-token')
