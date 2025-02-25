from django.contrib.auth.models import User
from django.db import models


# 회사 모델 (주식 종목)
class Company(models.Model):
  ticker = models.CharField(max_length=10, unique=True)  # 주식 티커 (예: AAPL)
  name = models.CharField(max_length=100)  # 회사 이름
  description = models.TextField(blank=True, null=True)  # 회사 설명
  category = models.CharField(max_length=50)  # 카테고리 (예: Tech, Finance)
  created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜


  def __str__(self):
    return f"{self.name} ({self.ticker}) - {self.category}"


class Author(models.Model):
  id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=50, unique=True)
  name = models.CharField(max_length=100, null=True, blank=True)
  description = models.TextField(blank=True, null=True, default="")
  profile_image_url = models.URLField(blank=True, null=True)
  companies = models.ManyToManyField(Company, related_name='authors')


# 트윗 모델
class Tweet(models.Model):
  id = models.AutoField(primary_key=True)
  tweet_url = models.CharField(max_length=200, null=True, blank=True)
  content = models.TextField()
  author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
  companies = models.ManyToManyField(Company, related_name="tweets")
  posted_at = models.DateTimeField()
  fetched_at = models.DateTimeField(auto_now_add=True)


# AI 분석 결과 모델
class AIAnalysis(models.Model):
  tweet = models.ForeignKey(Tweet,
                            on_delete=models.CASCADE,
                            related_name="ai_analyses")  # 분석 대상 트윗
  company = models.ForeignKey(Company,
                              on_delete=models.CASCADE,
                              related_name="ai_analyses")  # 분석 대상 회사
  ai_score = models.IntegerField(0)  # 긍정 점수 (0~1)
  summary = models.CharField(max_length=200, null=True, blank=True)
  reasoning = models.CharField(max_length=1000, null=True, blank=True)
  analyzed_at = models.DateTimeField(auto_now_add=True)  # 분석 시간

  class Meta:
    unique_together = ('tweet', 'company')  # 트윗과 회사 조합으로 고유성 보장


# 찬반 투표 모델
class Vote(models.Model):
  user = models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name="votes")  # 투표한 사용자
  ai_analysis = models.ForeignKey(AIAnalysis,
                                  on_delete=models.CASCADE,
                                  related_name="votes")  # 투표 대상 분석
  is_agree = models.BooleanField()  # 찬성(True) / 반대(False)
  voted_at = models.DateTimeField(auto_now_add=True)  # 투표 시간

  class Meta:
    unique_together = ('user', 'ai_analysis')  # 사용자당 분석별로 한 번만 투표 가능

  def __str__(self):
    return f"{self.user.username} voted {'Agree' if self.is_agree else 'Disagree'} on {self.ai_analysis}"


# 댓글 모델
class Comment(models.Model):
  user = models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name="comments")  # 댓글 작성자
  ai_analysis = models.ForeignKey(AIAnalysis,
                                  on_delete=models.CASCADE,
                                  related_name="comments")  # 댓글 대상 분석
  content = models.TextField()  # 댓글 내용
  created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

  def __str__(self):
    return f"Comment by {self.user.username} on {self.ai_analysis}"


# 사용자 모델에 관심 회사 추가 (Django User 확장)
class UserProfile(models.Model):
  user = models.OneToOneField(User,
                              on_delete=models.CASCADE,
                              related_name="profile")  # Django User와 1:1 연결
  followed_companies = models.ManyToManyField(
      Company, related_name="followers")  # 관심 회사들

  def __str__(self):
    return f"{self.user.username}'s Profile"


# 알림 모델
class Notification(models.Model):
  user = models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name="notifications")  # 알림 수신자
  company = models.ForeignKey(Company,
                              on_delete=models.CASCADE,
                              related_name="notifications")  # 관련 회사
  tweet = models.ForeignKey(Tweet,
                            on_delete=models.CASCADE,
                            related_name="notifications")  # 관련 트윗
  message = models.CharField(max_length=255)  # 알림 메시지
  is_read = models.BooleanField(default=False)  # 읽음 여부
  created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

  def __str__(self):
    return f"Notification for {self.user.username} about {self.company.ticker}"
