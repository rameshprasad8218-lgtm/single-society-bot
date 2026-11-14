"""Single Society bot settings. Edit freely."""
import os

PAGE_NAME = os.getenv("PAGE_NAME", "SINGLE SOCIETY")
PAGE_TAGLINE = "khabar, ekdum simple"
PAGE_HASHTAG = "#SingleSociety"

GN = "https://news.google.com/rss"
Q = "hl=hi&gl=IN&ceid=IN:hi"

FEEDS = {
    "top": f"{GN}?{Q}",
    "nation": f"{GN}/headlines/section/topic/NATION?{Q}",
    "business": f"{GN}/headlines/section/topic/BUSINESS?{Q}",
    "sports": f"{GN}/search?q=cricket&{Q}",
    "entertainment": f"{GN}/headlines/section/topic/ENTERTAINMENT?{Q}",
    "mehngai": f"{GN}/search?q=%E0%A4%A6%E0%A4%BE%E0%A4%AE+%E0%A4%AC%E0%A4%A2%E0%A4%BC%E0%A5%87+when:2d&{Q}",  # "daam badhe"
    "exam": f"{GN}/search?q=exam+result+OR+bharti+when:2d&{Q}",
    "local": f"{GN}/search?q=Uttarakhand+OR+%22Uttar+Pradesh%22+when:1d&{Q}",
}

# Series: name, tag shown on poster, feeds to read
SERIES = {
    "subah":    ("Subah Ki Chai",      "SUBAH KI CHAI",      ["top", "nation"]),
    "mehngai":  ("Mehngai Meter",      "MEHNGAI METER",      ["mehngai", "business"]),
    "exam":     ("Exam / Naukri Alert","EXAM ALERT",         ["exam"]),
    "cricket":  ("Cricket Ka Tadka",   "CRICKET KA TADKA",   ["sports"]),
    "bollywood":("Bollywood Masala",   "BOLLYWOOD MASALA",   ["entertainment"]),
    "shahar":   ("Apna Shahar",        "APNA SHAHAR",        ["local"]),
    "neta":     ("Neta Ji Ki Baatein", "NETA JI KI BAATEIN", ["nation", "top"]),
    "trending": ("Trending",           "TRENDING",           ["top", "nation", "entertainment", "sports"]),
}

# IST slot -> series rotation (index by day of year)
SLOTS = {  # 14 posts/day, every hour 8 AM - 9 PM IST
    "0800": ["subah"],
    "0900": ["mehngai", "exam"],
    "1000": ["trending"],
    "1100": ["cricket", "bollywood"],
    "1200": ["shahar"],
    "1300": ["neta", "trending"],
    "1400": ["bollywood", "cricket"],
    "1500": ["exam", "mehngai"],
    "1600": ["trending"],
    "1700": ["cricket", "bollywood"],
    "1800": ["neta", "shahar"],
    "1900": ["bollywood", "trending"],
    "2000": ["cricket", "mehngai"],
    "2100": ["trending"],
}

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
MAX_ITEMS_TO_AI = 12
