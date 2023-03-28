from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = [{
            'id': item['id'],
            'name': item['name']
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


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if not self.queryset.filter(id=user_id).exists():
            return Response({
                'data': {},
                'errors': [{'id': ['User does not exist']}],
                'code': status.HTTP_404_NOT_FOUND
            })
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
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
                'data': serializer.data,
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
