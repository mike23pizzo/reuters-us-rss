import requests
from bs4 import BeautifulSoup
from datetime import datetime
import email.utils as eut

URL = "https://www.reuters.com/world/us/"
r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

items = []

# Find article blocks - updated selector based on current site
for article in soup.select("article.story"):  # example selector; adjust if needed
    # Try to find headline link inside article
    a = article.find("a")
    if not a or not a.get("href"):
        continue

    title = a.get_text(strip=True)
    link = a["href"]
    if not link.startswith("http"):
        link = "https://www.reuters.com" + link

    # Try to find summary paragraph (optional)
    summary_tag = article.find("p")
    summary = summary_tag.get_text(strip=True) if summary_tag else title

    pub_date = eut.format_datetime(datetime.utcnow())

    items.append((title, link, summary, pub_date))

    if len(items) >= 10:
        break

# Build RSS XML
rss_items = ""
for title, link, desc, pub_date in items:
    # Escape XML special characters in title and description
    title_escaped = (title.replace("&", "&amp;")
                           .replace("<", "&lt;")
                           .replace(">", "&gt;"))
    desc_escaped = (desc.replace("&", "&amp;")
                         .replace("<", "&lt;")
                         .replace(">", "&gt;"))

    rss_items += f"""
    <item>
      <title>{title_escaped}</title>
      <link>{link}</link>
      <description>{desc_escaped}</description>
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
