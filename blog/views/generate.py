from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..ai_content.service import _generate_post


@api_view(["POST"])
def generate_post(request):
    title = request.data.get("title")
    tone = request.data.get("tone")

    try:
        result = _generate_post(title, tone)
        return Response(result, status=status.HTTP_200_ok)
    except ValueError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
