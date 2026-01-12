# 🇹🇭 Thai Digital Market Analyst (Local-First AI)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![CrewAI](https://img.shields.io/badge/AI-CrewAI-red) ![Vector DB](https://img.shields.io/badge/Database-SQLite--Vec-green) ![Status](https://img.shields.io/badge/Status-Operating_on_a_Prayer-yellow)

**A high-performance, local-first AI system designed to synthesize Thai digital market trends. It’s bilingual, it’s frugal, and it runs on hardware that really should be retired.**

This project operates on a "Local-First" philosophy. This is mostly because I value privacy and speed, but also because my internet connection is temperamental and I enjoy the illusion of control. It utilizes a Small Language Model (SLM) to analyze a curated local database of Thai news before reluctantly checking the broader internet. The result is high-quality, hallucination-free reporting running on an **M1 MacBook Air with 8GB of RAM**—a machine that wheezes if you open too many Chrome tabs.

---

## 🏗️ High-Performance Native AI in Restrictive Situations (Like Life in General)

Much like trying to host a dinner party in a studio apartment, this architecture is all about resource management and preventing a total meltdown. The system is engineered to squeeze every ounce of utility out of my limited RAM using a **Hybrid RAG (Retrieval-Augmented Generation)** strategy.

I initially used standard SQLite, which was fine, like instant coffee is fine. But then I discovered Vector Databases, which allow the computer to understand the *vibe* of a query, not just the keywords. Now, we are drinking espresso.

### 1. The Daily Scraper (`data/scraper.py`)
* **The Job:** Wakes up, drinks its digital juice, and scrapes the Thai internet so I don't have to doom-scroll manually.
* **The Sources:** TechSauce, Blognone, BrandInside, MarketingOops, PositioningMag, and the Bank of Thailand.
* **The Magic:** Unlike a boring standard scraper, this one calculates **AI Embeddings** (using `all-MiniLM-L6-v2`) on the fly. It converts text into mathematical vectors, storing them in `data/thai_news.db` using `sqlite-vec`.
* **The location:** All data lives safely in the `data/` folder, far away from the cloud.

### 2. The Hybrid Search Tool (`data/tools.py`)
* **The Gatekeeper:** This tool stands between the AI agent and the infinite chaos of the web.
* **The Logic:**
    1.  It checks our local Vector DB first. If you ask for "Digital Money," it intuitively finds "Virtual Banking," even if the words don't match. It understands *concepts*.
    2.  If—and only if—the local data is underwhelming (Distance score > 0.8), it sighs and performs a Google Search via `SerperDevTool`.
* **The Constraint:** It ruthlessly truncates content to 500 characters. We have 8GB of RAM; we cannot afford to be verbose.

### 3. The Sequential Analyst Agent (`data/test_hybrid_crew.py`)
* **The Brain:** A **Qwen 2.5 3B** model running via Ollama. It is surprisingly good at Thai, unlike me.
* **The Workflow:** It runs tasks in a strict sequence. We don't do multitasking here. Multitasking leads to memory swaps, and memory swaps lead to the spinning beach ball of death.
    1.  **Synthesize:** Read Thai news.
    2.  **Analyze:** Think about what it means.
    3.  **Report:** Write it down in English.
  
  It would look like this:

########################
## FINAL ENGLISH REPORT ##
########################

# Thailand Market Report - Fintech, Regulatory, E-commerce

## 1. Fintech Trends in Thailand

The fintech sector in Thailand is experiencing significant growth driven by digital payments, e-commerce, and financial inclusion. According to the Thailands Buy Now Pay Later (BNPL) market report from 2025, the BNPL payment market in Thailand is expected to grow by 14.9% annually, reaching US$3.94 billion by 2025. This growth can be attributed to three key catalysts: cross-border BNPL interoperability within Southeast Asia, B2B transactions, and consumer demand for digital payments.

## 2. Regulatory Updates in Thailand

Fintech regulation in Thailand is increasingly drawing the attention of both local entrepreneurs and foreign investors. The regulatory landscape has been evolving with proposed obligations including stronger seller verification, more active monitoring of listings, and clearer dispute handling mechanisms. These changes are aimed at ensuring a safer environment for businesses and consumers.

## 3. E-commerce Growth in Thailand

The e-commerce market in Thailand is projected to grow by 14% annually from 2024 to reach approximately 1.6 trillion baht by 2027, making it the second-largest market within ASEAN. Key drivers of this growth include advancements in digital payments and innovations like cross-border BNPL interoperability.

## 4. Digital Currencies and Green Investments

Thais are showing a keen interest in both digital currencies and green investments. UOB's FinTech in ASEAN research for 2021 indicates that Thai consumers have the highest awareness of green investments, with an openness to using digital platforms for such purposes. This trend is expected to continue as more businesses adopt sustainable practices.

## Conclusion

Thailand’s fintech sector is poised for substantial growth driven by innovative payment methods and e-commerce solutions. Regulatory frameworks are being strengthened to ensure a secure environment for both consumers and businesses. The country's growing interest in digital currencies and green investments further underscores its commitment to technological advancement and sustainability. These trends suggest that Thailand will continue to be an attractive market for foreign investors looking to capitalize on the region’s burgeoning fintech ecosystem.

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.10+** (The modern standard).
* **[Ollama](https://ollama.com/)** running locally.
* **`apsw`** (Because macOS hates standard SQLite extensions and we have to trick it).

### Installation

1.  **Clone the repository** (and authorize it, if your Mac allows you to do anything anymore):
    ```bash
    git clone [https://github.com/yourusername/thai-digital-analyst.git](https://github.com/yourusername/thai-digital-analyst.git)
    cd thai-digital-analyst
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Make sure `crewai`, `crawl4ai`, `sentence-transformers`, `apsw`, and `sqlite-vec` are in there. It’s a bit of a soup.)*

3.  **Pull the Model:**
    ```bash
    ollama pull qwen2.5:3b-instruct-q4_0
    ```

---

## 💻 Usage

### 1. Feed the Beast (Daily)
Run the scraper to populate your local database. It’s satisfying to watch it work while you drink coffee.
```bash
python data/scraper.py