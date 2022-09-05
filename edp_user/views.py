from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        status = request.POST.get('status')
        if username and email and password and role and status:
            user = UserProfile.objects.create_user(username=username, email=email, password=password, role=role,
                                                   status=status)
            return render(request, 'edp_index/index.html', {'user': user})


def user_logout(request):
    logout(request)
    request.session.flush()
    return render(request, 'edp_index/index.html')


def user_login(request):
    if request.method == 'GET':
        form = EDPUserLoginForm()
        return render(request, 'edp_user/login.html', {'form': form})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            # 用户验证
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                user = UserProfile.objects.get(username=user)
                return redirect(reverse('edp-index:index'), {'user': user})
            else:
                return render(request, 'edp_user/login.html', {'user': user})
        else:
            return render(request, 'edp_user/login.html', {'form': EDPUserLoginForm()})


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
