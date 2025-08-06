# backend/app/accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger('django')

class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                logger.error(f'Login failed: Missing username or password')
                return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                logger.info(f'Login successful for user: {username}')
                return Response({
                    'admin_token': token.key,
                    'is_admin': user.is_staff,
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f'Login failed: Invalid credentials for username {username}')
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VersionConfig(APIView):
    def get(self, request):
        try:
            return Response({"version": "1.0.0", "config": "example"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'VersionConfig error: {str(e)}')
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(APIView):
    def post(self, request):
        try:
            # 示例注册逻辑，需根据实际需求实现
            username = request.data.get('username')
            password = request.data.get('password')
            chatgpt_token = request.data.get('chatgpt_token')
            if not username or not password:
                logger.error(f'Register failed: Missing username or password')
                return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            # 这里应添加用户创建逻辑（如 User.objects.create_user）
            logger.info(f'Register not implemented for user: {username}')
            return Response({'error': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            logger.error(f'Register error: {str(e)}')
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginFreeView(APIView):
    def post(self, request):
        try:
            # 示例免费登录逻辑，需根据实际需求实现
            logger.info('LoginFree not implemented')
            return Response({'error': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            logger.error(f'LoginFree error: {str(e)}')
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)