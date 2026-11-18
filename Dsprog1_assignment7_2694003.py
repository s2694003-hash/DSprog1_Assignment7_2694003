import requests
from bs4 import BeautifulSoup

url = "https://github.com/orgs/google/repositories"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Webサーバーにリクエストを出す
res = requests.get(url, headers=header)
res.encoding = 'utf-8'  # 文字コードをUTF-8に変換する

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")