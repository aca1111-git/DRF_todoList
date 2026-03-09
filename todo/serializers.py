from rest_framework.serializers import ModelSerializer
from .models import Todo


# API 요청 데이터를 모델 객체로 변환하는 변환기
class TodoSerializer(ModelSerializer):
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


# 둘중 한개를 사용합니다.
