import requests
from bs4 import BeautifulSoup
import os


url="https://atcoder.jp/contests/abc423/tasks/abc423_a"
res=requests.get(url)
res.raise_for_status()
soup=BeautifulSoup(res.text,"html.parser")

for section in soup.select("section"):
    h3=section.find("h3")
    if not h3:
        continue
    title=h3.get_text(strip=True)
    if title.startswith("入力例"):
        print("input::::",section.find("pre").get_text("\n",strip=True))
    elif title.startswith("出力例"):
        print("output:::",section.find("pre").get_text("\n",strip=True))



