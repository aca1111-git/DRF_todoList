from django.urls import path
from .views.templates_views import TodoListView, TodoCreateView
from .views.api_views import TodoListAPI, TodoCreateAPI
from .views.templates_views import TodoDetailView, TodoUpdateView  # 추가
from .views.api_views import TodoRetrieveAPI, TodoUpdateAPI  # 추가

# from .views.templates_views import TodoDeleteView
from .views.api_views import TodoDeleteAPI

app_name = "todo"

urlpatterns = [
    # path("list/", views.todo_list, name="list"),  # 첫 테스트용
    # path("list/", views.TodoListView.as_view(), name="list"),
    # HTML 렌더링 뷰
    path("list/", TodoListView.as_view(), name="list"),
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("detail/<int:pk>/", TodoDetailView.as_view(), name="todo_Detail"),
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo_Update"),
    # api
    path("api/list/", TodoListAPI.as_view(), name="todo_api_list"),
    path("api/create/", TodoCreateAPI.as_view(), name="todo_api_create"),
    path("api/retrieve/<int:pk>/", TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
    path("api/update/<int:pk>/", TodoUpdateAPI.as_view(), name="todo_api_update"),
    path("api/delete/<int:pk>/", TodoDeleteAPI.as_view(), name="todo_api_delete"),
]
