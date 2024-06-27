import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import filedialog

# URLからHTMLを取得

url = ''
#権利面で不安なため省略
response = requests.get(url)
html = response.text

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(html, 'html.parser')

# 全ての記事を含む要素を見つける
articles = soup.find_all('dt')

# 記事データを格納するリスト
articles_data = []

for dt in articles:
	article_data = {}
	
	# 記事のURLからアーカイブIDを抽出
	pdf_link = dt.find('a', {'title': 'Download PDF'})
	if pdf_link:
		article_data['id'] = pdf_link.get('href').replace('/pdf/', '')

	# 記事のタイトルと概要を取得
	dd = dt.find_next_sibling('dd')
	if dd:
		# 著者を取得
		authors_div = dd.find('div', class_='list-authors')
		if authors_div:
			article_data['authors'] = ', '.join([a.text for a in authors_div.find_all('a')])

		title_div = dd.find('div', class_='list-title')
		if title_div:
			article_data['title'] = title_div.text.replace('Title:', '').strip()

	# 記事データをリストに追加
	articles_data.append(article_data)

df = pd.DataFrame(articles_data)
file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
if file_path:
    df.to_excel(file_path, index=False)
    print(f"Exported {len(articles_data)} items to {file_path}")
