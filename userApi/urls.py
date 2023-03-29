from django.urls import path, include

import api.urls

router = api.urls.ApiRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
