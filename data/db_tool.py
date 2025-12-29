import sqlite3
import os
from crewai_tools import BaseTool

class LocalNewsTool(BaseTool):
    name: str = "Local News Database"
    description: str = (
        "Useful for reading the latest scraped news about Thai Finance, "
        "Regulatory updates, and E-commerce. Use this BEFORE searching Google "
        "to get specific details from local sources like TechSauce, Blognone, and BOT."
    )

    def _run(self, query: str = None) -> str:
        """Fetch the latest 10 articles from the local DB"""
        # Auto-detect DB path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'market_data.db')
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get the most recent 10 articles
            # You can refine this SQL to filter by category if needed
            cursor.execute('''
                SELECT source, title, content, date_scraped 
                FROM news 
                ORDER BY date_scraped DESC 
                LIMIT 10
            ''')
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return "No local news found in database. You may need to run the scraper first."
            
            # Format into a string the LLM can read
            results = "HERE ARE THE LATEST LOCAL NEWS HIGHLIGHTS:\n\n"
            for row in rows:
                source, title, content, date = row
                # Truncate content to first 300 chars to save context window
                snippet = content[:300].replace('\n', ' ') + "..."
                results += f"- [{source}] {title} ({date})\n  Summary: {snippet}\n\n"
                
            return results
            
        except Exception as e:
            return f"Error reading database: {e}"
