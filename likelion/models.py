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


# 트윗 모델
class Tweet(models.Model):
  tweet_id = models.CharField(max_length=50, unique=True)  # X API에서 가져온 트윗 ID
  content = models.TextField()  # 트윗 내용
  author_name = models.CharField(max_length=100)  # 작성자 이름
  author_username = models.CharField(max_length=100)  # 작성자 사용자 이름 (@handle)
  author_profile_image = models.URLField(blank=True,
                                         null=True)  # 작성자 프로필 사진 URL
  companies = models.ManyToManyField(Company,
                                     related_name="tweets")  # 연관 회사들 (다대다)
  posted_at = models.DateTimeField()  # 트윗 게시 시간
  fetched_at = models.DateTimeField(auto_now_add=True)  # 데이터 수집 시간

  def __str__(self):
    return f"Tweet by {self.author_username}"


# AI 분석 결과 모델
class AIAnalysis(models.Model):
  tweet = models.ForeignKey(Tweet,
                            on_delete=models.CASCADE,
                            related_name="ai_analyses")  # 분석 대상 트윗
  company = models.ForeignKey(Company,
                              on_delete=models.CASCADE,
                              related_name="ai_analyses")  # 분석 대상 회사
  positive_score = models.FloatField()  # 긍정 점수 (0~1)
  negative_score = models.FloatField()  # 부정 점수 (0~1)
  buy_recommendation = models.FloatField()  # 매수 추천 퍼센트 (0~100)
  sell_recommendation = models.FloatField()  # 매도 추천 퍼센트 (0~100)
  analyzed_at = models.DateTimeField(auto_now_add=True)  # 분석 시간

  class Meta:
    unique_together = ('tweet', 'company')  # 트윗과 회사 조합으로 고유성 보장

  def __str__(self):
    return f"Analysis for {self.company.ticker} on Tweet {self.tweet.tweet_id}"


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
