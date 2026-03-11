# from rest_framework.views import APIView
from rest_framework import viewsets

from ..models import Todo  # 경로변경
from ..serializers import TodoSerializer  # 경로변경
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# 즉 todo 앱의 models.py 에서 정의된 모델을 가져옵니다.
from interaction.models import TodoLike, TodoBookmark, TodoComment
from rest_framework.decorators import action
from rest_framework.response import Response  # 👈 이 줄을 추가하세요!

# from rest_framework import status
from django.db.models import Q


# from .views.api_views import TodoViewSet


# class TodoListAPI(APIView):
#     def get(self, request):
#         # GET 요청이 들어오면 실행되는 함수

#         todos = Todo.objects.all()
#         # Todo 모델의 모든 데이터 조회 (QuerySet)

#         serializer = TodoSerializer(todos, many=True)
#         # 조회한 Todo 객체들을 Serializer로 JSON 변환 준비
#         # many=True → 여러 개의 객체를 변환한다는 의미

#         return Response(serializer.data)
#         # serializer.data를 JSON 형태로 변환하여 API 응답으로 반환


# class TodoCreateAPI(APIView):
#     def post(self, request):
#         serializer = TodoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         todo = serializer.save()
#         return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)


# class TodoRetrieveAPI(APIView):
#     def get(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당 todo 가 없어"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)


# class TodoUpdateAPI(APIView):
#     def put(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당 todo가 없어"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = TodoSerializer(todo, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         todo = serializer.save()
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)

#     def patch(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."},
#                 status=status.HTTP_404_NOT_FOUND,
#                 # HTTP 상태코드 404 반환
#             )
#         serializer = TodoSerializer(todo, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         todo = serializer.save()
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)


# class TodoDeleteAPI(APIView):
#     def delete(self, request, pk):

#         try:
#             todo = Todo.objects.get(pk=pk)

#         except Todo.DoesNotExist:
#             # 해당 Todo가 존재하지 않을 경우 실행

#             return Response(
#                 {"error": "해당하는 todo가 없습니다."},
#                 # 에러 메시지를 JSON 형태로 반환
#                 status=status.HTTP_404_NOT_FOUND,
#                 # HTTP 상태코드 404 (데이터 없음)
#             )

#         todo.delete()
#         # 조회한 Todo 데이터를 DB에서 삭제

#         return Response(status=status.HTTP_204_NO_CONTENT)
#         # 삭제 성공 시 응답 반환 (204 = 성공했지만 반환할 데이터 없음)


class TodoListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 50


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoListPagination

    def get_queryset(self):
        user = self.request.user

        return Todo.objects.filter(Q(is_public=True) | Q(user=user)).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_public=True)

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        # pagination 처리
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={"request": request},
            )

            return Response(
                {
                    "data": serializer.data,
                    "current_page": int(request.query_params.get("page", 1)),
                    "page_count": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link() is not None,
                    "previous": self.paginator.get_previous_link() is not None,
                }
            )
        # pagination 이 없는 경우
        serializer = self.get_serializer(
            qs,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "data": serializer.data,
                "current_page": 1,
                "page_count": 1,
                "next": False,
                "previous": False,
            }
        )

    # POST /todo/viewsets/view/<id>/like/
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):

        # 현재 Todo 가져오기
        todo = self.get_object()

        # 로그인한 사용자
        user = request.user

        # 좋아요 존재 확인
        obj, created = TodoLike.objects.get_or_create(todo=todo, user=user)

        # 새로 생성된 경우 → 좋아요 ON
        if created:
            liked = True

        # 이미 존재 → 삭제 → 좋아요 OFF
        else:
            obj.delete()
            liked = False

        # 전체 좋아요 개수 계산
        like_count = TodoLike.objects.filter(todo=todo).count()

        # 응답
        return Response({"liked": liked, "like_count": like_count})

    # POST /todo/viewsets/view/<id>/bookmark/
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):

        # 현재 Todo
        todo = self.get_object()

        # 로그인 사용자
        user = request.user

        # 북마크 생성 또는 조회
        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=user)

        # 북마크 ON
        if created:
            bookmarked = True

        # 북마크 OFF
        else:
            obj.delete()
            bookmarked = False

        # 전체 북마크 수
        bookmark_count = TodoBookmark.objects.filter(todo=todo).count()

        return Response({"bookmarked": bookmarked, "bookmark_count": bookmark_count})

    # POST /todo/viewsets/view/<id>/comments/
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):

        # Todo 가져오기
        todo = self.get_object()

        # 로그인 사용자
        user = request.user

        # 댓글 내용 가져오기
        content = (request.data.get("content") or "").strip()

        # 댓글 내용 검증
        if not content:
            return Response({"detail": "content is required"}, status=400)

        # 댓글 생성
        TodoComment.objects.create(todo=todo, user=user, content=content)

        # 댓글 개수 계산
        comment_count = TodoComment.objects.filter(todo=todo).count()

        return Response({"comment_count": comment_count})
