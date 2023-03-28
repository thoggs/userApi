from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def index(request, user_id=None):
    method = request.method
    match method:
        case 'GET':
            if user_id is None:
                users = User.objects.all().order_by('name')
                serializer = UserSerializer(users, many=True)
                data = [{
                    'id': item['id'],
                    'name': item['name']
                } for item in serializer.data]
                return Response({
                    'data': data,
                    'errors': [],
                    'code': status.HTTP_200_OK
                })
            else:
                try:
                    user = User.objects.get(id=user_id)
                    serializer = UserSerializer(user)
                    return Response({
                        'data': serializer.data,
                        'errors': [],
                        'code': status.HTTP_200_OK
                    })
                except User.DoesNotExist:
                    return Response({
                        'data': {},
                        'errors': [{'id': ['User does not exist']}],
                        'code': status.HTTP_404_NOT_FOUND
                    })
        case 'POST':
            serializer = UserSerializer(data=request.data)
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
        case 'PUT':
            try:
                user = User.objects.get(id=request.data['id'])
                serializer = UserSerializer(user, data=request.data)
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
            except User.DoesNotExist:
                return Response({
                    'data': {},
                    'errors': [{'id': ['User does not exist']}],
                    'code': status.HTTP_404_NOT_FOUND
                })
        case 'DELETE':
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response({
                    'data': {},
                    'errors': [{'id': ['User does not exist']}],
                    'code': status.HTTP_404_NOT_FOUND
                })
        case _:
            return Response({
                'data': [],
                'errors': [],
                'code': status.HTTP_404_NOT_FOUND
            })
