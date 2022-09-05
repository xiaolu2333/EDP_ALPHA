from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render

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
            user = UserProfile.objects.create_user(username=username,email=email,password=password, role=role, status=status)
            return render(request, 'edp_index/index.html')


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
                return render(request, 'edp_index/index.html', {'user': user})
            else:
                return render(request, 'edp_user/login.html', {'user': user})
        else:
            return render(request, 'edp_user/login.html', {'form': EDPUserLoginForm()})
