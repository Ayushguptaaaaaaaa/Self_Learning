
import requests


query=input("Enter the news topic you want to search for: ")

api_key="4b59ab429b154547990f91995599cc16"

url=f"https://newsapi.org/v2/everything?q={query}&from=2026-07-05&sortBy=publishedAt&apiKey={api_key}"

print(url)

r=requests.get(url)
data=r.json()
articles=data["articles"]

for index, article in enumerate(articles):
    print(f"{index + 1}. {article['title']} - {article['url']}")
    print("\n****************************************\n\n")