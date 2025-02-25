from django.shortcuts import render
from .models import Author, Company, Tweet, AIAnalysis, Vote, Comment, UserProfile, Notification
from django.db.models import Q
import requests


def index(request):
    ai_analysis = AIAnalysis.objects.get(id=35)
    authors = Author.objects.all()
    return render(request, 'likelion/index.html', {
        'ai_analysis': ai_analysis,
        'authors': authors
    })


def my_list(request):
    return render(request, 'likelion/my-list.html')


def my_profile(request):
    return render(request, 'likelion/my-profile.html')


def search(request):
    query = request.GET.get('q', '')

    tweets = Tweet.objects.filter(
        Q(content__icontains=query)
        | Q(author__username__icontains=query)) if query else []
    people = Author.objects.filter(
        Q(name__icontains=query)
        | Q(username__icontains=query)) if query else []
    companies = Company.objects.filter(
        Q(name__icontains=query) | Q(ticker__icontains=query)
        | Q(description__icontains=query)) if query else []

    # 로고 URL을 가져오기 위한 API 호출
    for company in companies:
        ticker = company.ticker
        api_url = f'https://api.twelvedata.com/logo?symbol={ticker}&apikey=c79378a0eb5b414fb3b8b54b84e64a06'
        response = requests.get(api_url)
        data = response.json()

        # 로고 URL을 company 객체에 저장 (또는 템플릿에서 바로 사용)
        company.logo_url = data.get('url', '')
    return render(
        request, 'likelion/search.html', {
            'tweets': tweets,
            'companies': companies,
            'people': people,
            'query': query,
        })


def ai_analysis(request):
    return render(request, 'likelion/ai-analysis.html')


def person(request):
    person_id = request.GET.get('q', '')
    person = Author.objects.get(id=person_id)
    # {
    #     name: "Elon Musk",
    #     username: "elonmusk",
    #     profile_image_url: "https://pbs.twimg.com/profile_images/1542248939/elon-musk-twitter"
    #    'description': "description",
    #    'companies': ['tesla', 'spacex', 'twitter']
    # }

    return render(request, 'likelion/person.html', {
        'person': person,
    })


def company(request, company_id):
    company_id = request.GET.get('q', '')
    company = Company.objects.filter(id=int(company_id))
    tweets = Tweet.objects.filter(companies=company)

    context = {
            'tweets': tweets,
            'companies': company,
    }
    return render(request, 'likelion/company.html', context)
