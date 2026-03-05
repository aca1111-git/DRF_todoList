from ..models import Todo  # 경로 변경
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

# def todo_list(request):  #  함수형
#     todos = Todo.objects.all()
#     return render(request, "todo/todo.html", {"todos": todos})

# class TodoListView(View): # 클래스형
#   def get(self, request):
#     todos = Todo.objects.all()
#     return render(request, "todo/todo.html", {"todos": todos})


# class TodoListGenericView(ListView): # 제너릭뷰
#     model = Todo
#     template_name = "todo/todo.html" # 기본값: todo_list.html
#     context_object_name = "todos"   # 기본값: object_list


class TodoListView(ListView):
    model = Todo  # 이 뷰가 사용할 모델 지정 (Todo 테이블 데이터를 조회)
    template_name = "todo/list.html"
    context_object_name = "todos"
    ordering = ["-created_at"]
    success_url = reverse_lazy("todo:list")


# 생성
class TodoCreateView(CreateView):
    model = Todo
    fields = ["name", "description", "complete", "exp"]
    # HTML form에서 입력받을 모델 필드 정의
    template_name = "todo/create.html"
    # Todo 생성 화면에 사용할 템플릿 파일
    success_url = reverse_lazy("todo:list")
    # 생성이 성공하면 이동할 URL (todo 목록 페이지)


class TodoDetailView(DetailView):
    model = Todo
    template_name = "todo/detail.html"
    context_object_name = "todo"


class TodoUpdateView(UpdateView):
    model = Todo
    fields = ["name", "description", "complete", "exp"]
    template_name = "todo/update.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo:list")
