from django.shortcuts import render


def index(request):
    user = request.user
    return render(request, 'edp_index/index.html', {'user': user})
