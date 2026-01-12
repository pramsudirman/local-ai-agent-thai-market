from crewai import Agent, Task, Crew, Process, LLM
from data.tools import HybridSearchTool

# 1. SETUP THE MODEL (Your Improved Config)
# This forces CrewAI to use the local Ollama instance directly
llm = LLM(
     model="ollama/qwen2.5:3b-instruct-q4_0",
     temperature=0.2,
     base_url="http://localhost:11434",
     max_retries=3,
     timeout=300.0,
)

# 2. SETUP THE TOOL
# This tool automatically checks your 'thai_news.db' first
market_tool = HybridSearchTool()

# 3. DEFINE THE AGENT
analyst = Agent(
    role="Senior Digital Analyst",
    goal="Synthesize Thai market trends into professional English reports.",
    backstory=(
        "You are an expert analyst who reads Thai local news "
        "and summarizes insights for international investors."
    ),
    tools=[market_tool],
    llm=llm,
    verbose=True
)

# 4. DEFINE THE TASK
# We explicitly force the "Thai Input -> English Output" workflow here
report_task = Task(
    description=(
        "1. Search for the latest trends in '{topic}'**specifically within the Thailand market**.\n"
        "2. The search tool will provide data from the local database or internet.\n"
        "3. Read the Thai content provided by the tool.\n"
        "4. Synthesize the key points and write a comprehensive report.\n"
        "5. IMPORTANT: Your final output MUST be in English."
    ),
    expected_output="A professional English market report (Markdown format) summarizing the findings.",
    agent=analyst
)

# 5. RUN THE CREW
if __name__ == "__main__":
    # You can change 'fintech' to 'ecommerce' or 'regulatory' to test different data
    topic = 'fintech', 'regulatory', 'ecommerce'
    
    crew = Crew(
        agents=[analyst],
        tasks=[report_task],
        process=Process.sequential,
        verbose=True
    )

    print(f"🚀 Starting Analyst Agent on topic: {topic}...")
    result = crew.kickoff(inputs={'topic': topic})
    
    print("\n\n########################")
    print("## FINAL ENGLISH REPORT ##")
    print("########################\n")
    print(result)