from django.conf import settings
from django.db import models


# ============================================
# Todo 좋아요 모델
# ============================================
class TodoLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todo = models.ForeignKey(
        "todo.Todo",  # 기존 todo 앱 모델 참조
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "todo")


# ============================================
# Todo 북마크 모델
# ============================================
class TodoBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "todo")


# ============================================
# Todo 댓글 모델
# ============================================
class TodoComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
