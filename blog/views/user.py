from rest_framework import viewsets, status

from ..serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['post'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

