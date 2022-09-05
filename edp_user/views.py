from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from edp_user.forms import UserRegisterForm, EDPUserLoginForm
from edp_user.models import UserProfile


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


from edp_user.serializers import UserInfoSerializer
from rest_framework.renderers import JSONRenderer



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
def user_serializer(request):
    # 序列化
    if request.method == 'GET':
        user_info = UserProfile.objects.all()
        serializer = UserInfoSerializer(user_info, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=400)
