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

# 取得したHTMLをgithub-google.htmlファイルに書き込む（タグの構造を確認するため）
with open("github-google.html", "w", encoding="utf-8") as f:
    f.write(res.text)

# HTMLのソースコードをBeautifulsoup4オブジェクトに変換する
html_soup = BeautifulSoup(res.text, 'html.parser')

# リポジトリ1件ごと（<li>）に、名前・主要な言語・スターの数を取り出す
for li in html_soup.select('ul[data-listview-component="items-list"] > li'):
    name = li.select_one('h3 a span').get_text(strip=True)

    lang_tag = li.select_one('span[class*="PrimaryLanguageName"]')
    language = lang_tag.get_text(strip=True) if lang_tag else None  # 言語がない場合はNone

    star_tag = li.select_one('a[href$="/stargazers"]')
    stars = star_tag.get_text(strip=True) if star_tag else "0"

    print(name, language, stars)
