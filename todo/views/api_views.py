# from rest_framework.views import APIView
from rest_framework import viewsets

from ..models import Todo  # 경로변경
from ..serializers import TodoSerializer  # 경로변경
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

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
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoListPagination

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
