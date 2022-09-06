from django.contrib.auth import logout, login, authenticate, hashers
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from edp_user.forms import UserRegisterForm, EDPUserLoginForm
from edp_user.models import UserProfile
from edp_user.serializers import UserInfoSerializer


def index(request):
    user = request.user
    return render(request, 'edp_user/index.html', {'user': user})


def user_register(request):
    """用户注册"""
    if request.method == 'GET':
        register_form = UserRegisterForm()
        return render(request, 'edp_user/register.html', {'form': register_form})
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.cleaned_data.pop('confirm_password')  # 清楚该字段
            register_form.cleaned_data['password'] = hashers.make_password(
                register_form.cleaned_data['password'])  # 密码加密
            user = UserProfile(**register_form.cleaned_data)  # 实例化模型
            try:
                user.save()  # 保存模型实例
            except IntegrityError:  # 捕获整合错误：因为User 模型默认 username 保持唯一性
                raise ValidationError(  # 抛出注册表单自定义的异常
                    register_form.error_messages['username_existed']
                )
            # 不向模板传递 user 上下文时，模板仍然可使用 user 来代表当前用户对象（基于登陆信息，但因此会缺少用户模型中的其他信息）
            return render(request, 'edp_index/index.html', {'user': user})


def user_logout(request):
    """用户登出"""
    logout(request)
    request.session.flush()
    return render(request, 'edp_index/index.html')


def user_login(request):
    """用户登陆"""
    if request.method == 'POST':
        login_form = EDPUserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            # 用户验证
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # 获取完整的用户信息
                user = UserProfile.objects.filter(username=username).first()
                return redirect(reverse('edp-index:index'), {'user': user})
            else:
                return render(request, 'edp_user/login.html', {'form': EDPUserLoginForm()})
        else:
            return render(request, 'edp_user/login.html', {'form': EDPUserLoginForm()})
    login_form = EDPUserLoginForm()
    return render(request, 'edp_user/login.html', {'form': login_form})


@api_view(['GET', 'POST'])
@login_required
def user_list(request):
    """用户信息列表"""
    # 序列化
    if request.method == 'GET':
        user_info = UserProfile.objects.all()
        serializer = UserInfoSerializer(user_info, many=True)
        return Response(serializer.data)
    # 反序列化
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required
def user_detail(request, pk):
    """用户信息详情"""
    try:
        user_info = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserInfoSerializer(user_info)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(user_info, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
