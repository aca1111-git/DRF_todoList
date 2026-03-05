from django.test import TestCase
from rest_framework.test import APIClient

from ..models import Todo


class TodoAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.todo = Todo.objects.create(
            name="운동",
            description="스쿼드 10개",
            complete=False,
            exp=10,
        )

    def test_list(self):
        res = self.client.get("/todo/api/list/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_create(self):  # 생성 테스트 (POST /create/)
        payload = {
            "name": "공부",
            "description": "DRF",
            "complete": False,
            "exp": 5,
        }

        # 새 Todo 생성 요청
        res = self.client.post("/todo/api/create/", payload, format="json")

        # 상태코드가 201(생성 성공)인지 확인
        self.assertEqual(res.status_code, 201)

        # 기존 1개 + 새로 생성 1개 = 총 2개인지 확인
        self.assertEqual(Todo.objects.count(), 2)

    def test_retrieve(self):
        # 생성된 Todo의 id로 조회
        res = self.client.get(f"/todo/api/retrieve/{self.todo.id}/")

        # 상태코드 200 확인
        self.assertEqual(res.status_code, 200)

        # 반환된 데이터의 name 값이 올바른지 확인
        self.assertEqual(res.json()["name"], "운동")

    def test_update_patch(self):  # 수정 테스트
        payload = {"name": "운동(수정)"}

        # 해당 Todo의 name 수정 요청
        res = self.client.patch(
            f"/todo/api/update/{self.todo.id}/", payload, format="json"
        )

        # 상태코드 200 확인
        self.assertEqual(res.status_code, 200)

        # DB에서 다시 불러와서 실제 값이 변경되었는지 확인
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, "운동(수정)")

    def test_delete(self):
        # 삭제 요청
        res = self.client.delete(f"/todo/api/delete/{self.todo.id}/")

        # 상태코드 204(삭제 성공) 확인
        self.assertEqual(res.status_code, 204)

        # 실제 DB에 해당 데이터가 존재하지 않는지 확인
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_not_found_returns_404(self):
        # 존재하지 않는 id로 조회
        res = self.client.get("/todo/api/retrieve/999999/")

        # 404(Not Found) 반환 확인
        self.assertEqual(res.status_code, 404)


"""
1. GET `/todo/api/list/` → 200 + 리스트가 온다
2. POST `/todo/api/create/` → 201 + 생성됨
3. GET `/todo/api/retrieve/<pk>/` → 200 + 해당 todo
4. PATCH `/todo/api/update/<pk>/` → 200 + 값 변경됨
5. DELETE `/todo/api/delete/<pk>/` → 204 + 삭제됨
"""
