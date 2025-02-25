from django.shortcuts import render


def index(request):
    return render(request, 'likelion/index.html')

def my_list(request):
    return render(request, 'likelion/my-list.html')
    
def my_profile(request):
    return render(request, 'likelion/my-profile.html')

def search(request):
    return render(request, 'likelion/search.html')

def person(request):
    return render(request, 'likelion/person.html')

def company(request):
    return render(request, 'likelion/company.html')
