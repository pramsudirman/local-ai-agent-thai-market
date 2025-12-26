import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool

# === DUMMY KEY - MUST BE FIRST ===
# Prevents CrewAI from crashing by checking for OpenAI key
os.environ["OPENAI_API_KEY"] = "sk-proj-dummykey1234567890abcdef"

# === M1 8GB OPTIMIZED LOCAL LLM ===
local_llm = LLM(
    model="ollama/qwen2.5:3b-instruct-q4_0",
    temperature=0.2,
    base_url="http://localhost:11434",
    max_retries=3,
    timeout=300.0,
    # CRITICAL ADDITION: Increases context window to 4096 tokens.
    # Without this, the model "forgets" the English report before it finishes translating.
    options={"num_ctx": 4096} 
)

# === SEARCH TOOL ===
search_tool = SerperDevTool()

# === AGENT ===
# We use the same agent for both tasks to save memory
thai_analyst = Agent(
    role="Senior Thai Digital Markets Analyst",
    goal="Research Thailand's e-commerce, virtual banking, and lending markets",
    backstory="""
    You are a veteran financial analyst with 10+ years covering Southeast Asian digital markets.
    You are an expert in translating complex financial concepts between English and Thai.
    Your expertise includes:
    - Bank of Thailand (BOT) virtual banking license framework
    - E-commerce GMV tracking (Shopee, Lazada, TikTok Shop)
    - Alternative lending analysis
    """,
    tools=[search_tool],
    llm=local_llm,
    verbose=True,
    memory=False,           # Disable OpenAI embeddings
    allow_delegation=False, # Disable agent-to-agent calls
    max_iter=3,
)

# === TASK 1: RESEARCH & ENGLISH DRAFT ===
# Focuses ONLY on gathering data and writing the English part
english_research_task = Task(
    description="""
    Generate a comprehensive Thai digital landscape report covering:

    1. **E-COMMERCE (2024 data with 2025-2027 projections):**
       - Market size & growth
       - Top 3 platforms (Shopee, Lazada, TikTok) with market share
       - Search: "bot.or.th ecommerce 2025", "Statista Thailand e-commerce 2025"
    
    2. **VIRTUAL BANKING (2024-2025 regulatory landscape):**
       - BOT licensing status & timeline
       - Key consortium applicants (CP Group, Gulf, SCB, etc.)
       - Search: "bot.or.th virtual bank license 2025", "KPMG Thailand virtual banks"
    
    3. **DIGITAL LENDING:**
       - Market size & NPL rates vs traditional banks
       - Search: "Alternative lending Thailand 2025", "BOT financial stability report"

    **OUTPUT REQUIREMENT:** Produce a professional report in **ENGLISH ONLY**. 
    Include specific numbers, dates, and citations (Source: ...).
    Make all headers bold.
    """,
    agent=thai_analyst,
    expected_output="A full English market report with citations.",
)

# === TASK 2: TRANSLATION (Simplified) ===
translation_task = Task(
    description="""
    You will receive a market report in English.
    
    1. Translate the content into professional Thai (Business/Formal tone).
    2. Use correct Thai terms for "Virtual Banking" (ธนาคารไร้สาขา) and "NPL" (หนี้เสีย).
    3. Keep numbers, company names, and citations in English.
    
    **OUTPUT REQUIREMENT:** Output **ONLY** the Thai translation. Do not include the original English text.
    Start with the header: # **รายงานภาษาไทย**
    """,
    agent=thai_analyst,
    context=[english_research_task],
    expected_output="The Thai translation of the report.",
)

# === CREW CONFIGURATION ===
crew = Crew(
    agents=[thai_analyst],
    tasks=[english_research_task, translation_task], # Runs research first, then translation
    process=Process.sequential,
    verbose=True,
    planning=False,
    memory=False,
)