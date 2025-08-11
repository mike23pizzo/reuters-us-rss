import requests
from bs4 import BeautifulSoup
from datetime import datetime
import email.utils as eut

URL = "https://www.reuters.com/world/us/"
r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

# Collect top articles
items = []
for article in soup.select("article a[data-testid='Heading']"):
    title = article.get_text(strip=True)
    link = article["href"]
    if not link.startswith("http"):
        link = "https://www.reuters.com" + link
    desc = title  # Could expand with more scraping if needed
    pub_date = eut.format_datetime(datetime.utcnow())
    items.append((title, link, desc, pub_date))
    if len(items) >= 10:
        break

# Build RSS XML
rss_items = ""
for title, link, desc, pub_date in items:
    rss_items += f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <description>{desc}</description>
      <pubDate>{pub_date}</pubDate>
      <guid isPermaLink="true">{link}</guid>
    </item>"""

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Reuters — United States</title>
    <link>{URL}</link>
    <description>Top U.S. headlines from Reuters (auto-generated)</description>
    <language>en-us</language>
    <lastBuildDate>{eut.format_datetime(datetime.utcnow())}</lastBuildDate>
    {rss_items}
  </channel>
</rss>
"""

with open("docs/reuters-us.xml", "w", encoding="utf-8") as f:
    f.write(rss)
