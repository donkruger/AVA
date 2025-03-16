import requests

url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=JSE.PPE&apikey=9RGHAR0LD0OCYIJW'
r = requests.get(url)
data = r.json()

print(data)