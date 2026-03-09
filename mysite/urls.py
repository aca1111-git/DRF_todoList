from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("todo/", include(("todo.urls", "todo"))),  # 딕셔너리로 해주니 오류 안남
    path("", include("accounts.urls")),
    path("", lambda request: redirect("todo:list")),  # 첫페이지가 무조건 보이게하기
]

# ✅ [추가] DEBUG일 때만 media 파일을 /media/로 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
