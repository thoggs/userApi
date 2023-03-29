from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import User
from api.serializers import UserSerializer, ObtainTokenSerializer


class ObtainTokenViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = ObtainTokenSerializer
    queryset = User.objects.none()
    name = 'obtain-token'

    def list(self, request, *args, **kwargs):
        return Response({
            "data": {},
            "errors": [{"message": "Method \"GET\" not allowed"}],
            "code": status.HTTP_405_METHOD_NOT_ALLOWED
        })

    def create(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            data = {
                "token": response.data["access"]
            }
            return Response({
                "data": data,
                "errors": [],
                "code": status.HTTP_200_OK
            })
        except Exception as e:
            return Response({
                "data": {},
                "errors": [{"message": str(e)}],
                "code": status.HTTP_400_BAD_REQUEST
            })


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'users'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = [{
            'id': item['id'],
            'name': item['name'],
            'email': item['email']
        } for item in serializer.data]
        return Response({
            'data': data,
            'errors': [],
            'code': status.HTTP_200_OK
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'errors': [],
                'code': status.HTTP_201_CREATED
            })
        else:
            return Response({
                'data': {},
                'errors': serializer.errors,
                'code': status.HTTP_400_BAD_REQUEST
            })

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if not self.queryset.filter(id=user_id).exists():
            return Response({
                'data': {},
                'errors': [{'id': ['User does not exist']}],
                'code': status.HTTP_404_NOT_FOUND
            })
        instance = self.queryset.get(id=user_id)
        serializer = self.get_serializer(instance)
        return Response({
            'data': {
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'email': serializer.data['email']
            },
            'errors': [],
            'code': status.HTTP_200_OK
        })

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if not self.queryset.filter(id=user_id).exists():
            return Response({
                'data': {},
                'errors': [{'id': ['User does not exist']}],
                'code': status.HTTP_404_NOT_FOUND
            })

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': {
                    'id': serializer.data['id'],
                    'name': serializer.data['name'],
                    'email': serializer.data['email']
                },
                'errors': [],
                'code': status.HTTP_200_OK
            })
        else:
            return Response({
                'data': {},
                'errors': serializer.errors,
                'code': status.HTTP_400_BAD_REQUEST
            })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'data': {},
            'errors': [],
            'code': status.HTTP_204_NO_CONTENT
        })
