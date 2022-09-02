from django.shortcuts import render


def index(request):
    return render(request, 'edp_index/index.html')
