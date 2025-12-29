import sqlite3
import os
from crewai_tools import BaseTool, SerperDevTool

class HybridSearchTool(BaseTool):
    name: str = "Hybrid Market Search"
    description: str = (
        "Always use this tool to find Thai market data. "
        "It checks the internal database first, and searches the internet only if needed."
    )

    def _run(self, query: str) -> str:
        print(f"\n🔎 Searching for: '{query}'")
        
        # 1. SEARCH LOCAL DB
        # We search for keywords in both Title and Content
        db_results = self._search_sqlite(query)
        
        # 2. CHECK "COMPLETENESS"
        # If we found at least 3 good articles locally, we trust the DB.
        if len(db_results) >= 3:
            print(f"   ✓ Found {len(db_results)} articles in Local DB. Using them.")
            return self._format_results(db_results, source="Local Database (Internal)")
        
        # 3. IF INCOMPLETE -> SEARCH INTERNET
        # If we have 0-2 results, we append Google Search results to fill the gap.
        print(f"   ⚠️ Only found {len(db_results)} local articles. Expanding search to Internet...")
        
        serper = SerperDevTool()
        web_results = serper.run(search_query=query)
        
        # Combine Local + Web
        local_text = self._format_results(db_results, source="Local Database")
        return f"{local_text}\n\n=== ADDITIONAL INTERNET FINDINGS ===\n{web_results}"

    def _search_sqlite(self, query):
        """Finds relevant rows in thai_news.db"""
        # Determine path dynamically
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'data', 'thai_news.db')
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Simple keyword match
            sql = """
                SELECT title, summary, source_domain, scraped_at 
                FROM news 
                WHERE title LIKE ? OR full_content LIKE ?
                ORDER BY scraped_at DESC 
                LIMIT 5
            """
            wildcard = f"%{query}%"
            cursor.execute(sql, (wildcard, wildcard))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"   ❌ DB Error: {e}")
            return []

    def _format_results(self, results, source):
        if not results:
            return ""
        
        formatted = f"=== SOURCE: {source} ===\n"
        for title, summary, domain, date in results:
            formatted += f"• TITLE: {title}\n"
            formatted += f"  DATE: {date}\n"
            formatted += f"  SOURCE: {domain}\n"
            # We assume the summary/content is in Thai, the Agent will translate it
            formatted += f"  CONTENT: {summary}\n\n"
        return formatted
