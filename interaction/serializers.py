from rest_framework import serializers
from .models import TodoLike, TodoBookmark, TodoComment


# ============================================
# Todo 좋아요 Serializer
# ============================================
class TodoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoLike
        fields = "__all__"


# ============================================
# Todo 북마크 Serializer
# ============================================
class TodoBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoBookmark
        fields = "__all__"


# ============================================
# Todo 댓글 Serializer
# ============================================
class TodoCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username", read_only=True  # 유저가 수정할수 없음(조회용)
    )

    class Meta:
        model = TodoComment
        fields = [
            "id",
            "todo",
            "user",
            "username",
            "content",
            "created_at",
        ]
        read_only_fields = ["user"]
