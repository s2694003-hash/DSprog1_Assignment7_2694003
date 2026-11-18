import sqlite3

db_name = "github_google_repositories.db"

conn = sqlite3.connect(db_name)
cur = conn.cursor()

# 保存したデータをSELECT文で表示する
print("---- 保存したリポジトリの件数 ----")
cur.execute("SELECT COUNT(*) FROM repositories")
print(cur.fetchone()[0])

print("---- スターの多い順（上位20件） ----")
cur.execute("SELECT name, language, stars FROM repositories ORDER BY stars DESC LIMIT 20")
for name, language, stars in cur.fetchall():
    print(f"{name:40} {str(language):15} {stars:>8}")

print("---- 言語ごとのリポジトリ数（上位10件） ----")
cur.execute("""
    SELECT language, COUNT(*) FROM repositories
    GROUP BY language ORDER BY COUNT(*) DESC LIMIT 10
""")
for language, n in cur.fetchall():
    print(f"{str(language):15} {n:>5}")

# print("---- 保存したデータ（全件） ----")
# cur.execute("SELECT * FROM repositories")
# for row in cur.fetchall():
#     print(row)

conn.close()