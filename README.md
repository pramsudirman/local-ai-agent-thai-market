# simple-local-ai-agent-thai-market

🇹🇭 The "Christmas Itch" Thai Digital Analyst

(Or: How I spent my holiday arguing with a 3B model instead of eating fruitcake)
Most people spend their Christmas weekend reconsidering their life choices or hiding from relatives. I spent mine developing a persistent "itch"—the kind that can only be scratched by staying up until 3:00 AM wondering why a machine with the collective knowledge of humanity keeps trying to answer me in Mandarin when I specifically asked for Thai.

This project is the result of that itch. It is a weekly automated dispatch delivered to your inbox every Monday morning, providing a comprehensive report on the Thai Digital Landscape (e-commerce, virtual banking, and lending).

It is also, for the record, 100% free.

----

🛠 The "I Have No Budget" Tech Stack
Building an AI agent is quite easy when you have a supercomputer and a venture capital firm paying your electric bill. It is significantly more "charming" when you are doing it on a MacBook Air M1 with 8GB of RAM.

Because my laptop has the memory capacity of a caffeinated squirrel, I had to make some choices:

The Brains: Ollama running Qwen2.5:3b. Why 3b? Because if I run anything larger, the fanless Air starts to emit a smell like a toaster oven, and my keyboard becomes hot enough to sear a scallop.

The Muscle: CrewAI. It coordinates the "agents," which is just a fancy way of saying it keeps the AI from wandering off and talking about something else.

The Eyes: Serper.dev. It scours the Thai internet so I don't have to.

The Glue: Python and a very fragile main.py script that acts as a final filter to remove any unexpected Chinese characters (Qwen has... identity issues).

[!TIP] A Small Note on Hardware: If you find this project useful and feel a surge of holiday spirit, I am currently accepting donations in the form of a MacBook M4 with 32GB of RAM. Think of it as a humanitarian effort to save my current laptop from an early, molten grave. Lol.

----

🇹🇭 Why Bilingual? (The "Second Month" Ambition)
You might ask, "Why bother with a Thai version?"

Well, I am currently in my second month of private Thai lessons. As anyone who has attempted to learn a tonal language knows, it is a process defined by high-stakes humiliation. By forcing my AI agent to produce reports in both English and Thai, I am essentially forcing myself to read Thai business terminology while I drink my Monday coffee.

It’s efficient. It’s ambitious. It’s probably going to result in me accidentally ordering a virtual bank license when I meant to order a pad kra pao.

----
📬 Get the Report
If you’d like to receive these weekly reports (and witness the gradual improvement of both my Thai and my agent’s sanity), drop your email here:
