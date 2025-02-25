from django.contrib import admin
from .models import AIAnalysis, Author, Comment, Company, Notification, Tweet, UserProfile, Vote

# 기본 등록, Tweet, AIAnalysis, Vote, Comment, UserProfile, Notification
admin.site.register(Company)
admin.site.register(Author)
admin.site.register(Tweet)
admin.site.register(AIAnalysis)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Notification)
