from rest_framework import viewsets, status

from ..serializers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
