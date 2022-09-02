from django.shortcuts import render

from edp_user.forms import UserRegisterForm


def index(request):
    return render(request, 'edp_user/index.html')


def user_register(request):
    """用户注册"""
    if request.method == 'GET':
        register_form = UserRegisterForm()
        return render(request, 'edp_user/register.html', {'form': register_form})
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            return render(request, 'edp_index/index.html', {'user': user})

#
# def log_in(request):
#     if request.method == 'GET':
#         form = EDPUserLoginForm()
#         return render(request, 'edp_user_management/login.html', {'form': form})
#     if request.method == 'POST':
#         form = EDPUserLoginForm(request.POST)
#         print(request.POST)
#         print("1111111111")
#         if form.is_valid():
#             print("2222222222222")
#             user = EDPUser.objects.get(username=form.cleaned_data['username'])
#             if user is not None and user.check_password(form.cleaned_data['password']):
#                 print("3333333333")
#                 login(request, request.user)
#                 return render(request, 'edp_index/index.html', {'user': user})
#             else:
#                 return reverse('edp_index:index')
#         else:
#             error_message = form.errors
#             print(error_message)
#             context = {
#                 'error_message': error_message,
#                 'form': EDPUserLoginForm()
#             }
#             return render(request, 'edp_user_management/login.html', context)
