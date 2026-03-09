# from django.shortcuts import render
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignupSerializer


class SignupAPIView(APIView):
    # 회원가입은 JWT/세션과 무관하게 그대로 사용

    # 로그인하지 않은 사용자도 접근 가능
    permission_classes = [AllowAny]

    # POST 요청 처리
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 검증 완료 후 사용자 생성
        serializer.save()
        # 회원가입 성공 응답
        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


class SessionLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # POST 요청 처리
    def post(self, request):
        # 현재 로그인된 사용자 세션 종료
        logout(request)
        # 로그아웃 성공 응답
        return Response({"detail": "로그아웃(세션정리)"}, status=status.HTTP_200_OK)
