# Simple Local AI agent for Thai market

🇹🇭 The "Christmas Itch" Thai Digital Analyst

(Or: How I spent my holiday arguing with a 3B model instead of eating fruitcake)
Most people spend their Christmas weekend reconsidering their life choices or hiding from relatives. I spent mine developing a persistent "itch"—the kind that can only be scratched by staying up until 3:00 AM wondering why a machine with the collective knowledge of humanity keeps trying to answer me in Mandarin when I specifically asked for Thai.

This project is the result of that itch. It is a weekly automated dispatch delivered to your inbox every Monday morning, providing a comprehensive report on the Thai Digital Landscape (e-commerce, virtual banking, and lending).

It is also, for the record, 100% free. It would show something like this on your email:

<img width="1110" height="509" alt="image" src="https://github.com/user-attachments/assets/f7f7531c-2837-4b94-a5e5-7ef633added6" />
<img width="1115" height="428" alt="image" src="https://github.com/user-attachments/assets/80158a21-ba35-4f09-ba9e-7ae3197a83c3" />
<img width="1118" height="506" alt="image" src="https://github.com/user-attachments/assets/ba18bab0-fa8a-44be-adea-f7de5d98cd46" />
<img width="1117" height="509" alt="image" src="https://github.com/user-attachments/assets/89967eda-bf4a-4cbd-94e7-87637f7dcf0f" />


----

🛠 The "I Have No Budget" Tech Stack
--
Building an AI agent is quite easy when you have a supercomputer and a venture capital firm paying your electric bill. It is significantly more "charming" when you are doing it on a MacBook Air M1 with 8GB of RAM.

Because my laptop has the memory capacity of a caffeinated squirrel, I had to make some choices:

The Brains: Ollama running Qwen2.5:3b. Why 3b? Because if I run anything larger, the fanless Air starts to emit a smell like a toaster oven, and my keyboard becomes hot enough to sear a scallop.

The Muscle: CrewAI. It coordinates the "agents," which is just a fancy way of saying it keeps the AI from wandering off and talking about something else.

The Eyes: Serper.dev. It scours the Thai internet so I don't have to.

The Glue: Python and a very fragile main.py script that acts as a final filter to remove any unexpected Chinese characters (Qwen has... identity issues).

[!TIP] A Small Note on Hardware: If you find this project useful and feel a surge of holiday spirit, I am currently accepting donations in the form of a MacBook M4 with 32GB of RAM. Think of it as a humanitarian effort to save my current laptop from an early, molten grave. Lol. JK

----

🇹🇭 Why Bilingual? (The "Second Month" Ambition)
--
You might ask, "Why bother with a Thai version?"

Well, I am currently in my second month of private Thai lessons. As anyone who has attempted to learn a tonal language knows, it is a process defined by high-stakes humiliation. By forcing my AI agent to produce reports in both English and Thai, I am essentially forcing myself to read Thai business terminology while I drink my Monday coffee.

It’s efficient. It’s ambitious. It’s probably going to result in me accidentally ordering a virtual bank license when I meant to order a pad kra pao.

----
📬 Get the Report
--
If you’d like to receive these weekly reports (and witness the gradual improvement of both my Thai and my agent’s sanity), drop your email here:
https://airtable.com/app0mzmjk6SConlTo/pag0ntw9HNnMcYFJw/form


----
🧠 How It Works (The Architecture)
--
Because my MacBook Air starts hyperventilating if it tries to think in two languages simultaneously, I had to get creative with the architecture.

I couldn't just ask the AI to "Research in English and then translate to Thai" in one breath. It would inevitably forget what it was doing halfway through, or worse, start hallucinating Chinese characters out of sheer confusion.

Instead, I use a two-step sequential process with a manual stitch. It goes like this:

<img width="1499" height="3065" alt="Mermaid Chart - Create complex, visual diagrams with text -2025-12-26-090840" src="https://github.com/user-attachments/assets/47ee315a-5851-435e-a5eb-7fbfdf94c74e" />

⚙️ Installation (Join the 8GB Club)
-
Want to run this locally and heat up your own apartment? Here is how to get it running on constrained hardware.

Prerequisites:
- Python 3.10+
- Ollama (for running local models)
- A Serper.dev API key (free tier is fine for weekly runs)
- An SMTP email account (like Gmail app password) to send the results.

Step 1: The Local LLM Setup (Crucial)
---
First, download and install Ollama.

Next, open your terminal. We need to pull the specific model that strikes the balance between "actually smart" and "won't crash an M1 Air." That model is Qwen 2.5 3B (Quantized 4-bit).

Run this command:
```
ollama pull qwen2.5:3b-instruct-q4_0
```
Warning: Do not get cocky and try to pull the 7B or 14B versions unless you have the RAM to back it up. My agent is explicitly coded to look for this specific 3B model tag.

Step 2: Clone and Venv
--
```
git clone [your-repo-url-here]
cd thai-digital-analyst
python -m venv venv
source venv/bin/activate  # (On Windows use: venv\Scripts\activate)
```

Step 3: Install Dependencies
--
```
pip install -r requirements.txt
```
(Note for you: Make sure you generate a requirements.txt containing: crewai, crewai-tools, langchain-ollama, python-dotenv, and whatever email library you used).

Step 4: Environment Variables
--
Duplicate the .env.example file to .env:

cp .env.example .env
Populate your .env file. It should look something like this:

```
#THE FAKE KEY (Required by CrewAI to not crash, even though we don't use it)
OPENAI_API_KEY=sk-proj-dummykey1234567890abcdef
#THE REAL KEYS
SERPER_API_KEY=your_actual_serper_key_here
# EMAIL CONFIG (For sending the report)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_app_specific_password
RECIPIENT_EMAIL=where.the.report.goes@email.com
```
Step 5: Run It
--
Take a deep breath, ensure Ollama is running in the background, and run:

```
python src/main.py
```
Go grab a coffee. It takes about 3-5 minutes on the M1 Air. If everything works, you'll see the console producing research, then translation, and finally, a fresh email in your inbox.

License
--
MIT. Go wild. Just don't blame me if the AI hallucinates that TikTok has bought the Bank of Thailand.
