from blog.models import Post
from .utils import validate_text_input
from ..client import ContentClient
import logging

logger = logging.getLogger(__name__)


def summarize_builder(content: str) -> str:
    prompt = f"Summarize the following blog post:\n{content}"
    return prompt


def summarize_post(post_id: int) -> dict:

    if type(post_id) is not int or post_id <= 0:
        raise ValueError("Post ID must be a positive integer.")

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise ValueError("Post not found.")

    cleaned_content = validate_text_input(
        post.content, min_length=20, field_name="Content"
    )
    if len(cleaned_content) > 500:
        raise ValueError("Post content must not exceed 500 characters.")


    prompt = summarize_builder(cleaned_content)
    client=ContentClient()
    try:
        summary = client.generate(prompt)
    except Exception:
        logger.exception("Failed to summarize post %s", post_id)
        raise

    if not summary or not summary.strip():
        raise ValueError("Summary is empty.")
    return {
        "post_id": post_id,
        "summary": summary.strip(),
        "length": len(summary.strip()),
    }
