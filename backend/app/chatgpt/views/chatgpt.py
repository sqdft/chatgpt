from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.chatgpt.models import ChatgptAccount, ChatgptCar
from app.chatgpt.serializers import ShowChatgptTokenSerializer, AddChatgptTokenSerializer, ChatGPTLoginSerializer, \
    UpdateChatgptInfoSerializer, DeleteChatgptAccountSerializer
from app.page import DefaultPageNumberPagination
from app.settings import CHATGPT_GATEWAY_URL
from app.utils import save_visit_log, req_gateway, get_client_ip
from app.accounts.models import User
from rest_framework.exceptions import ValidationError


class ChatGPTAccountEnum(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        result = ChatgptAccount.objects.filter(auth_status=True).order_by("-id").values(
            "id", "chatgpt_username", "plan_type").all()
        return Response({"data": result})


class ChatGPTAccountView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        queryset = ChatgptAccount.objects.order_by("-id").all()
        pg = DefaultPageNumberPagination()
        pg.page_size_query_param = "page_size"
        page_accounts = pg.paginate_queryset(queryset, request=request)
        chatgpt_list = [i.chatgpt_username for i in page_accounts]

        try:
            use_count_dict = req_gateway("post", "/api/get-chatgpt-use-count", json={"chatgpt_list": chatgpt_list})
        except:
            use_count_dict = {}
        serializer = ShowChatgptTokenSerializer(instance=page_accounts, use_count_dict=use_count_dict, many=True)
        return pg.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        # 录入 chatgpt 账号
        serializer = AddChatgptTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for chatgpt_token in serializer.data["chatgpt_token_list"]:
            if not chatgpt_token:
                continue
            res_json = req_gateway("post", "/api/get-user-info", json={"chatgpt_token": chatgpt_token})
            res_json["auth_status"] = True
            ChatgptAccount.save_data(res_json)

            # 关闭记忆
            chatgpt_name = res_json["user_info"]["email"]
            req_gateway("post", "/api/close-chatgpt-memory", json={"chatgpt_name": chatgpt_name})

        return Response({"message": "录入成功"})

    def put(self, request):
        serializer = UpdateChatgptInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ChatgptAccount.objects.filter(chatgpt_username=serializer.data["chatgpt_username"]).update(
            remark=serializer.data["remark"])
        return Response({"message": "更新gpt信息成功"})

    def delete(self, request):
        serializer = DeleteChatgptAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gpt_obj = ChatgptAccount.objects.filter(chatgpt_username=serializer.data["chatgpt_username"]).first()
        if gpt_obj:
            car_obj = ChatgptCar.objects.filter(gpt_account_list=[gpt_obj.id], car_name__contains="reg_").first()
            if car_obj:
                User.objects.filter(gptcar_list=[car_obj.id]).delete()
                car_obj.delete()
            gpt_obj.delete()

        return Response({"message": "删除成功"})


class ChatGPTLoginView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChatGPTLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip = get_client_ip(request)

        user_gpt_list = ChatgptAccount.get_by_gptcar_list(request.user.gptcar_list)
        user_gpt_id_list = [i.id for i in user_gpt_list]

        if serializer.data["chatgpt_id"] not in user_gpt_id_list:
            raise ValidationError("该账号不属于当前用户")

        chatgpt = ChatgptAccount.get_by_id(serializer.data["chatgpt_id"])
        user_name = request.user.username + ip if request.user.username == "free_account" else request.user.username
        payload = {
            "user_name": user_name,
            "access_token": chatgpt.access_token,
            "isolated_session": request.user.isolated_session,
            "limits": request.user.model_limit
        }
        # print(payload)
        res_json = req_gateway("post", "/api/login", json=payload)

        save_visit_log(request, "choose-gpt", chatgpt.chatgpt_username)

        return Response(res_json)
