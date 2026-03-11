from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Todo
from interaction.models import TodoLike, TodoBookmark, TodoComment


# API 요청 데이터를 모델 객체로 변환하는 변환기
class TodoSerializer(ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    like_count = serializers.SerializerMethodField()
    # 현재 사용자가 좋아요 했는지 여부
    is_liked = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    # 현재 사용자가 북마크 했는지 여부
    is_bookmarked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = [
            "id",
            "name",
            "description",
            "complete",
            "exp",
            "image",
            "created_at",
            "user",
            "username",
            "is_public",
            "like_count",
            "is_liked",
            "bookmark_count",
            "is_bookmarked",
            "comment_count",
        ]
        read_only_fields = ["user"]

        # fields = [
        #     "name",
        #     "description",
        #     "complete",
        #     "exp",
        #     "completed_at",
        #     "created_at",
        #     "updated_at",
        #     "image",
        #     "user",
        # ]

        # exclude = ["created_at", "updated_at"]
        # 모든 필드를 기본 포함시키고 → 특정 필드만 제외하고 싶을 때

    # 현재 로그인 사용자 가져오는 함수
    def _user(self):
        # serializer context에서 request 가져오기
        request = self.context.get("request")
        # 로그인 상태 확인
        if request and request.user.is_authenticated:
            return request.user
        # 로그인 안 된 경우
        return None

    def get_like_count(self, obj):
        return TodoLike.objects.filter(todo=obj).count()

    def get_is_liked(self, obj):

        # 현재 로그인 사용자
        user = self._user()

        # 로그인 안한 경우
        if not user:
            return False
        # 좋아요 존재 여부 확인
        return TodoLike.objects.filter(todo=obj, user=user).exists()

    def get_bookmark_count(self, obj):
        return TodoBookmark.objects.filter(todo=obj).count()

    def get_is_bookmarked(self, obj):

        # 현재 사용자
        user = self._user()

        if not user:
            return False

        return TodoBookmark.objects.filter(todo=obj, user=user).exists()

    def get_comment_count(self, obj):

        return TodoComment.objects.filter(todo=obj).count()
