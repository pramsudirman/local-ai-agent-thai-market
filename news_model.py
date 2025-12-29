import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

@dataclass
class NewsArticle:
    url: str
    title: str
    raw_content: str
    category: str = "general"
    published_date: str = None
    
    def __post_init__(self):
        # 1. Clean Title
        self.title = self.title.strip().replace('\n', ' ')
        
        # 2. Clean Content (Strip HTML & Spaces)
        clean_text = re.sub(r'<[^>]+>', '', self.raw_content)
        self.clean_content = re.sub(r'\s+', ' ', clean_text).strip()
        
        # 3. Generate Unique ID (MD5 of URL)
        self.id = hashlib.md5(self.url.encode()).hexdigest()
        
        # 4. Extract Source Domain
        self.source = urlparse(self.url).netloc.replace('www.', '')
        
        # 5. Default Date
        if not self.published_date:
            self.published_date = datetime.now().strftime('%Y-%m-%d')

    def to_tuple(self):
        """Format for SQLite insertion"""
        return (
            self.id,
            self.title,
            self.clean_content[:500],  # Summary
            self.clean_content,        # Full Content
            self.url,
            self.source,
            self.published_date,
            self.category,
            datetime.now().isoformat()
        )