import apsw
import sqlite_vec
import json
import os
from crewai_tools import BaseTool, SerperDevTool
from sentence_transformers import SentenceTransformer

class HybridSearchTool(BaseTool):
    name: str = "Hybrid Market Search"
    description: str = (
        "Search for Thai market news. Uses AI semantic search to find concepts "
        "even if words don't match. Always checks local DB first, then Google if needed."
    )

    def _run(self, query: str) -> str:
        print(f"\n🔎 Searching for: '{query}'")
        
        # 1. Load AI Model
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query_vector = model.encode(query).tolist()
        except Exception as e:
            return f"Error loading embedding model: {e}"

        # 2. Connect to DB
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'data', 'thai_news.db')
        
        conn = apsw.Connection(db_path)
        conn.enableloadextension(True)
        conn.loadextension(sqlite_vec.loadable_path())
        
        cursor = conn.cursor()
        
        # 3. Perform Semantic Search
        sql = """
            SELECT n.title, n.summary, v.distance, n.source_domain, n.scraped_at
            FROM vec_news v
            JOIN news n ON v.news_id = n.id
            WHERE v.embedding MATCH ? AND k = 5
            ORDER BY v.distance
        """
        
        try:
            results = list(cursor.execute(sql, (json.dumps(query_vector),)))
        except Exception as e:
            print(f"   ❌ Database Search Error: {e}")
            conn.close()
            return self._fallback_to_web(query)

        conn.close()

        # 4. Smart Decision
        if not results:
            print("   ⚠️ Database empty or no matches. Going to Internet...")
            return self._fallback_to_web(query)

        best_score = results[0][2]
        
        # Threshold: < 0.8 means we found something somewhat relevant
        if best_score < 0.8:
            print(f"   ✓ Found relevant local news (Score: {best_score:.2f}). Using DB.")
            return self._format_results(results)
        else:
            print(f"   ⚠️ Weak match (Score: {best_score:.2f}). Expanding search...")
            return self._fallback_to_web(query, local_results=results)

    def _fallback_to_web(self, query, local_results=None):
        """Helper to run Google Search and combine with any weak local results"""
        
        # We forcibly append "Thailand" to the search query if it's not already there.
        if "thai" not in query.lower():
            search_query = f"{query} Thailand market news"
        else:
            search_query = query
            
        print(f"   🌍 Triggering Google Search for: '{search_query}'")
        web_content = SerperDevTool().run(search_query=search_query)
        
        report = ""
        if local_results:
            report += self._format_results(local_results, source="Local DB (Weak Match)")
            report += "\n\n=== 🌍 EXPANDED INTERNET SEARCH ===\n"
        
        report += web_content
        return report

    def _format_results(self, results, source="Local Database (Semantic Match)"):
        formatted = f"=== SOURCE: {source} ===\n"
        for title, summary, dist, domain, date in results:
            formatted += f"• TITLE: {title}\n"
            formatted += f"  SOURCE: {domain} ({date})\n"
            formatted += f"  RELEVANCE: {round((1-dist)*100)}%\n" 
            formatted += f"  CONTENT: {summary}\n\n"
        return formatted