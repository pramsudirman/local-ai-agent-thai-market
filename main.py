import os
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# Connect to your local Llama3 model
llama3 = Ollama(model="llama3")

# Define your Analyst Agent (The "Artist" Profile)
analyst = Agent(
  role='Senior Fintech Product Analyst',
  goal='Analyze the Virtual Bank landscape in Thailand for Ascend Group',
  backstory='''You are an expert in ASEAN Fintech with 10 years of experience. 
  You specialize in behavior-led banking and inclusive digital ecosystems.''',
  verbose=True,
  allow_delegation=False,
  llm=llama3
)

# Define the Task
research_task = Task(
  description='''Identify 3 key trends in Thai Virtual Banking for 2026. 
  Focus on AI-driven credit scoring and mobile user experience.''',
  expected_output='A 3-paragraph strategic summary for a Head of Product.',
  agent=analyst
)

# Form the Crew
crew = Crew(
  agents=[analyst],
  tasks=[research_task],
  process=Process.sequential
)

# Execute!
result = crew.start()
print(result)
