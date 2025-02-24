from django.shortcuts import render


def index(request):
    return render(request, 'likelion/index.html')

def my_profile(request):
    return render(request, 'likelion/my-profile.html')
