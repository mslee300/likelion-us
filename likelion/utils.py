import os
import json
from django.core.exceptions import ValidationError
from .models import Company, Tweet, AIAnalysis
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from datetime import datetime
import tweepy

openai_api_key = os.environ.get('OPENAI_API_KEY')
x_api_token = os.environ.get('X_API_TOKEN')
client = tweepy.Client(bearer_token=x_api_token)

llm = ChatOpenAI(model="gpt-4o-mini",
                 temperature=0.5,
                 openai_api_key=openai_api_key)

analysis_template = ChatPromptTemplate.from_messages([("system", """
        You are an AI expert analyzing the impact of social media tweets on the stock market. 
        Given a tweet and a stock ticker, evaluate the likelihood of a stock price change within 24 hours as a score between 0 and 1. The score is interpreted as follows:
        - 100: The stock price is highly likely to rise
        - -100: The stock price is highly likely to fall
        - 0: The likelihood of rising or falling is irrelavant, uncertain, or volatility is expected

        Consider the following factors in your analysis:
        - The influence of the tweet's author (e.g., CEO, politician, etc.)
        - How directly the tweet relates to the ticker
        - Market sentiment and political/economic context
        - Balance positive and negative factors evenly
        - Avoid excessive optimism or pessimism, maintaining a realistic judgment

        Return the output in the following JSON format:
            "ai_score": a score between -100 and 100,
            "sumamry": a summary of the analysis,
            "reasoning": "Explanation of the analysis in natural and concise English"
        

        Input data:
        - 'tweet': 
            - name: author, 
            - content: tweet text, 
            - date: posting date
        - 'ticker': the stock ticker to analyze
        """),
                                                      ("human", """
        tweet: {tweet}
        ticker: {ticker}
        """)])

related_companies_template = ChatPromptTemplate.from_messages([("system", """
    You are an advanced AI designed to analyze social media posts and identify related publicly traded companies based on their content. 
    
    Your task is to extract and return a list of stock tickers (e.g., TSLA, AAPL) for companies that are directly or indirectly referenced, implied, or contextually relevant in the provided tweet. Consider the author's influence, the tweet's subject matter, and any companies likely impacted by the statement. 
    
    Return the tickers as a simple list, such as ["TSLA", "AAPL", "AMZN"]. If no specific companies are identified, infer plausible ones based on context and the author's known affiliations or industries.

    Input data:
    - 'tweet': 
        - name: author, 
        - content: tweet text, 
        - date: posting date
    """), ("human", """
    tweet: {tweet}
    """)])

analysis_chain = analysis_template | llm
related_companies_chain = related_companies_template | llm


def save_ai_analysis():
    tweets = Tweet.objects.all()
    for tweet in tweets:
        tweet_data = {
            "author": tweet.author.name,
            "content": tweet.content,
            "date": tweet.posted_at.strftime("%Y-%m-%d, %H:%M:%S")
        }

        response = related_companies_chain.invoke({
            "tweet": tweet_data,
        }).content

        tickers = json.loads(response)

        for ticker in tickers:
            if Company.objects.filter(ticker=ticker).exists():
                response = analysis_chain.invoke({
                    "tweet": tweet_data,
                    "ticker": ticker
                }).content
                print(tweet_data["author"], tweet_data["content"], ticker,
                      response)
                if response["ai_score""] != 0:
                    


def get_ai_score_from_tweet(tweet, ticker):
    return chain.invoke({"tweet": tweet, "ticker": ticker}).content


def add_companies_from_json(json_file_path):
    """
    JSON 파일에서 회사 데이터를 읽어 데이터베이스에 추가하는 함수.

    Args:
        json_file_path (str): JSON 파일 경로 (예: 'companies.json')
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            companies_data = json.load(file)

        for company_data in companies_data:
            ticker = company_data.get('symbol')
            name = company_data.get('name')
            description = company_data.get('description')
            category = company_data.get('category')

            # 필수 필드 확인
            if not ticker or not name or not category:
                print(f"Skipping invalid data: {company_data}")
                continue

            # 이미 존재하는 회사 업데이트 또는 생성
            try:
                company, created = Company.objects.update_or_create(
                    ticker=ticker,
                    defaults={
                        'name': name,
                        'description': description,
                        'category': category,
                    })
                if created:
                    print(f"Created new company: {name} ({ticker})")
                else:
                    print(f"Updated existing company: {name} ({ticker})")
            except ValidationError as e:
                print(f"Validation error for {ticker}: {e}")
            except Exception as e:
                print(f"Error processing {ticker}: {e}")

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {json_file_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def get_latest_tweet():  # username: str, bearer_token: str
    """
    Fetches the latest tweet from the given username using Twitter API.
    """
    username = "elonmusk"
    bearer_token = x_api_token
    client = tweepy.Client(bearer_token=bearer_token)

    try:
        # Fetch user information by username to get the user ID
        user = client.get_user(username=username)
        user_id = user.data.id

        # Retrieve the most recent tweets (min required is 5)
        tweets = client.get_users_tweets(id=user_id, max_results=5)
        print(tweets.data)
        if tweets.data:
            latest_tweet = tweets.data[0]  # Select the most recent tweet
            print(f"Latest Tweet Fetched: {latest_tweet.text}")  # DEBUG PRINT
            return {
                'tweet_id': latest_tweet.id,
                'text': latest_tweet.text,
                'created_at': latest_tweet.created_at
            }
        else:
            return {'error': 'No tweets found for this user.'}

    except tweepy.TweepyException as e:
        return {'error': str(e)}


def delete_tweets():
    AIAnalysis.objects.all().delete()
