from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..ai_content.service.summarizer import summarize_post


@api_view(["POST"])
def summarize_post_view(request, post_id):
    try:
        result = summarize_post(post_id)

        return Response(result, status=status.HTTP_200_OK)

    except ValueError as exc:
        if str(exc) == "Post not found.":
            return Response(
                {"error": str(exc)},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"error": str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )