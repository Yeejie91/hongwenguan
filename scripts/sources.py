"""Education news sources used by news_scraper.py.

Add / remove entries here to control what shows up on news.html.
Each source is a dict with: name, region, lang, url (RSS / Atom).
Google News RSS (`news.google.com/rss/search?q=...`) is preferred for sites
that don't expose their own feed - it's stable, legal, and aggregates well.
"""

SOURCES = [
    # ===== 马来西亚 / 新加坡 中文 =====
    {"name": "星洲日报 · 教育", "region": "马来西亚", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:sinchew.com.my+%E6%95%99%E8%82%B2&hl=zh-CN&gl=MY&ceid=MY:zh-Hans"},
    {"name": "东方日报 · 教育", "region": "马来西亚", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:orientaldaily.com.my+%E6%95%99%E8%82%B2&hl=zh-CN&gl=MY&ceid=MY:zh-Hans"},
    {"name": "中国报 · 教育", "region": "马来西亚", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:chinapress.com.my+%E6%95%99%E8%82%B2&hl=zh-CN&gl=MY&ceid=MY:zh-Hans"},
    {"name": "光明日报 · 教育", "region": "马来西亚", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:guangming.com.my+%E6%95%99%E8%82%B2&hl=zh-CN&gl=MY&ceid=MY:zh-Hans"},
    {"name": "联合早报 · 教育", "region": "新加坡", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:zaobao.com.sg+%E6%95%99%E8%82%B2&hl=zh-CN&gl=SG&ceid=SG:zh-Hans"},

    # ===== 中港台 =====
    {"name": "人民日报 · 教育", "region": "中国", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:people.com.cn+%E6%95%99%E8%82%B2&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"},
    {"name": "中国教育报", "region": "中国", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:jyb.cn+%E6%95%99%E8%82%B2&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"},
    {"name": "明报 · 教育", "region": "香港", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:mingpao.com+%E6%95%99%E8%82%B2&hl=zh-HK&gl=HK&ceid=HK:zh-Hant"},
    {"name": "联合报 · 教育", "region": "台湾", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:udn.com+%E6%95%99%E8%82%B2&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
    {"name": "亲子天下", "region": "台湾", "lang": "zh",
     "url": "https://news.google.com/rss/search?q=site:parenting.com.tw+%E6%95%99%E8%82%B2&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},

    # ===== 日韩 =====
    {"name": "Japan Times · Education", "region": "Japan", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:japantimes.co.jp+education&hl=en-US&gl=JP&ceid=JP:en"},
    {"name": "The Mainichi · Education", "region": "Japan", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:mainichi.jp+education&hl=en-US&gl=JP&ceid=JP:en"},
    {"name": "Korea Herald · Education", "region": "Korea", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:koreaherald.com+education&hl=en-US&gl=KR&ceid=KR:en"},
    {"name": "Korea Times · Education", "region": "Korea", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:koreatimes.co.kr+education&hl=en-US&gl=KR&ceid=KR:en"},

    # ===== 全球英文教育媒体 =====
    {"name": "BBC Education", "region": "Global", "lang": "en",
     "url": "https://feeds.bbci.co.uk/news/education/rss.xml"},
    {"name": "The Guardian · Education", "region": "Global", "lang": "en",
     "url": "https://www.theguardian.com/education/rss"},
    {"name": "Times Higher Education", "region": "Global", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:timeshighereducation.com&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Inside Higher Ed", "region": "Global", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:insidehighered.com&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Education Week", "region": "Global", "lang": "en",
     "url": "https://news.google.com/rss/search?q=site:edweek.org&hl=en-US&gl=US&ceid=US:en"},
]

REGION_GROUPS = {
    "南洋（马新）": ["马来西亚", "新加坡"],
    "中港台": ["中国", "香港", "台湾"],
    "日韩": ["Japan", "Korea"],
    "全球": ["Global"],
}
