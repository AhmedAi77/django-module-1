from rest_framework import serializers

from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id",)

    def validate(self, data):
        if not data.get("author"):
            raise serializers.ValidationError({"author": "This field is required."})

        if not data.get("post"):
            raise serializers.ValidationError({"post": "This field is required."})

        return data
