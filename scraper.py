import asyncio
import sqlite3
import os
import hashlib
import re
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler

# ==========================================
# 1. CONFIGURATION: The "Beat" (Target Sites)
# ==========================================
# These are the specific sites you want to monitor for your report.
TARGETS = [
    # --- FINTECH & MARKET TRENDS ---
    {
        "url": "https://techsauce.co/en/financial-technology", 
        "category": "fintech",
        "source": "TechSauce"
    },
    {
        "url": "https://www.blognone.com/topics/fintech",
        "category": "fintech",
        "source": "Blognone"
    },
    {
        "url": "https://brandinside.asia/category/finance-market/",
        "category": "market_trends",
        "source": "BrandInside"
    },
    {
        "url": "https://positioningmag.com/category/insight",
        "category": "market_trends",
        "source": "PositioningMag"
    },
    
    # --- E-COMMERCE ---
    {
        "url": "https://www.marketingoops.com/category/digital-transformation/ecommerce/",
        "category": "ecommerce",
        "source": "MarketingOops"
    },
    {
        "url": "https://www.etda.or.th/en/Knowledge-Sharing/e-Commerce-Survey-Insights.aspx",
        "category": "ecommerce",
        "source": "etda"
    },
    
    # --- REGULATORY (Bank of Thailand) ---
    {
        "url": "https://www.bot.or.th/th/news-and-media/news.html",
        "category": "regulatory",
        "source": "Bank of Thailand"
    }
]

# ==========================================
# 2. SETUP PATHS
# ==========================================
# We auto-detect the project root to ensure we save to data/thai_news.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True) # Create folder if it doesn't exist
DB_PATH = os.path.join(DATA_DIR, 'thai_news.db')

# ==========================================
# 3. DATA MODEL (The Cleaner)
# ==========================================
@dataclass
class NewsArticle:
    url: str
    title: str
    raw_content: str
    source_domain: str
    category: str = "general"
    
    def __post_init__(self):
        # A. CLEAN TITLE
        self.title = self.title.strip().replace('\n', ' ')
        
        # B. CLEAN CONTENT (Strip HTML-like artifacts & excessive spaces)
        # remove markdown links like [text](url) -> text
        clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', self.raw_content) 
        # remove multiple spaces/newlines
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        self.clean_content = clean_text
        
        # C. GENERATE ID (MD5 Hash of URL)
        # We append the date to the URL to create a unique ID per day.
        # This allows us to re-scrape the same "News Feed" page tomorrow without error,
        # but prevents duplicates if you run the script twice today.
        unique_string = f"{self.url}-{datetime.now().strftime('%Y-%m-%d')}"
        self.id = hashlib.md5(unique_string.encode()).hexdigest()
        
        # D. TIMESTAMP
        self.scraped_at = datetime.now().isoformat()

    def to_tuple(self):
        """Format for SQLite insertion"""
        return (
            self.id,
            self.title,
            self.clean_content[:500],  # Summary (First 500 chars)
            self.clean_content,        # Full Content
            self.url,
            self.source_domain,
            self.scraped_at,
            self.category
        )

# ==========================================
# 4. DATABASE MANAGER
# ==========================================
def init_db():
    """Ensure the table exists with the correct schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id TEXT PRIMARY KEY,
            title TEXT,
            summary TEXT,
            full_content TEXT,
            url TEXT,
            source_domain TEXT,
            scraped_at TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(article: NewsArticle):
    """Save article to DB, ignoring if ID already exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT OR IGNORE INTO news VALUES (?,?,?,?,?,?,?,?)''', 
            article.to_tuple()
        )
        conn.commit()
        return cursor.rowcount > 0 # Returns True if actually inserted
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return False
    finally:
        conn.close()

# ==========================================
# 5. THE ENGINE (Crawl4AI)
# ==========================================
async def run_scraper():
    print(f"🤖 Intern Bot waking up... Target: {len(TARGETS)} sites")
    print(f"📂 Saving to: {DB_PATH}")
    
    # 1. Initialize Database
    init_db()
    
    # 2. Start Crawling
    async with AsyncWebCrawler(verbose=True) as crawler:
        for target in TARGETS:
            print(f"\nScanning: {target['source']}...")
            
            try:
                # bypass_cache=True forces a fresh network call
                result = await crawler.arun(url=target['url'], bypass_cache=True)
                
                if not result.markdown:
                    print("   ⚠️ No content found (Empty response).")
                    continue

                # 3. Process & Clean
                # We limit raw_content to 10k chars to prevent database bloat
                article = NewsArticle(
                    url=target['url'],
                    title=f"Daily Brief: {target['source']}",
                    raw_content=result.markdown[:10000], 
                    source_domain=target['source'],
                    category=target['category']
                )
                
                # 4. Save
                if save_to_db(article):
                    print(f"   ✅ Saved new data for {target['source']}")
                else:
                    print(f"   zzz Data already exists for today.")
                    
            except Exception as e:
                print(f"   ❌ Failed to crawl {target['source']}: {e}")

    print("\n🏁 Scrape finished. Data is ready for the Analyst Agent.")

if __name__ == "__main__":
    asyncio.run(run_scraper())