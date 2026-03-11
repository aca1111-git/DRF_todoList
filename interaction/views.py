from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from todo.models import Todo
from .models import TodoLike, TodoBookmark, TodoComment
from .serializers import TodoCommentSerializer

# from django.shortcuts import render


class TodoLikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        obj, created = TodoLike.objects.get_or_create(todo=todo, user=request.user)

        if not created:
            obj.delete()
            liked = False

        else:
            liked = True

        count = TodoLike.objects.filter(todo=todo).count()

        return Response({"liked": liked, "like_count": count})


# =========================================================
# 북마크 토글 API
# POST /interaction/bookmark/<todo_id>/
# =========================================================
class TodoBookmarkToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=request.user)
        if not created:
            obj.delete()
            bookmarked = False
        else:
            bookmarked = True

        count = TodoBookmark.objects.filter(todo=todo).count()
        return Response(
            {
                "bookmarked": bookmarked,  # 현재 북마크 상태
                "bookmark_count": count,  # 전체 북마크 수
            }
        )


# =========================================================
# 댓글 등록 API
# POST /interaction/comment/<todo_id>/
# =========================================================
class TodoCommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        content = request.data.get("content", "").strip()

        if not content:
            return Response({"detail": "내용이 필요합니다."}, status=400)
        comment = TodoComment.objects.create(
            todo=todo, user=request.user, content=content
        )
        serializer = TodoCommentSerializer(comment)
        return Response(serializer.data)


# =========================================================
# 댓글 목록 조회 API
# GET /interaction/comment/<todo_id>/
# =========================================================
class TodoCommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id)
        # 최신 댓글이 먼저 나오도록 정렬
        comments = TodoComment.objects.filter(todo=todo).order_by("-created_at")

        # 댓글 목록을 serializer로 변환
        serializer = TodoCommentSerializer(
            comments, many=True  # 여러 개 객체이기 때문에 many=True
        )
        # JSON 응답 반환
        return Response(serializer.data)
