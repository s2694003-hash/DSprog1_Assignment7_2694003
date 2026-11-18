import requests
from bs4 import BeautifulSoup
import time

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

    
# 指定したページのHTMLを取得してBeautifulSoupオブジェクトに変換する
def get_page(page):
    try:
        res = requests.get(url, params={'page': page}, headers=header, timeout=10)
        res.raise_for_status()
        res.encoding = 'utf-8'  # 文字コードをUTF-8に変換する
    except requests.RequestException as e:
        print(f"取得失敗:{page}ページ目 ({e})")
        return None
    finally:
        time.sleep(1)  # サーバーへの負荷軽減のため1秒間スリープする
    return BeautifulSoup(res.text, 'html.parser')


# 1. 1ページ目を取得し、ページ送りのリンクから最後のページ番号を取得する
html_soup = get_page(1)
page_links = html_soup.select('a[data-component="Pagination.Page"]')
last_page = max(int(a.get_text(strip=True)) for a in page_links)
print(f"全{last_page}ページ")

count = 0
for page in range(1, last_page + 1):
    if page > 1:
        html_soup = get_page(page)
        if html_soup is None:
            continue

    # 2. リポジトリ1件ごと（<li>）に、名前・主要な言語・スターの数を取り出す
    for li in html_soup.select('ul[data-listview-component="items-list"] > li'):
        name = li.select_one('h3 a span').get_text(strip=True)

        lang_tag = li.select_one('span[class*="PrimaryLanguageName"]')
        language = lang_tag.get_text(strip=True) if lang_tag else None  # 言語がない場合はNone

        star_tag = li.select_one('a[href$="/stargazers"]')
        stars = star_tag.get_text(strip=True) if star_tag else "0"

        print(name, language, stars)
        count += 1

    print(f"{page}/{last_page}ページ目:{count}件")

print(f"完了:{count}件")
