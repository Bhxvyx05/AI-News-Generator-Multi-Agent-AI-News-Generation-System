# 📰 AI News Generator: Multi-Agent AI News Generation System

<p align="center">

![Project](https://img.shields.io/badge/AI%20NEWS%20GENERATOR-MULTI--AGENT-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=for-the-badge)
![LLM](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

### 🚀 Transform Any Topic into a Professional AI-Generated News Article with Realistic Illustrations

**Search • Summarize • Write • Visualize**

[Features](#-key-features) •
[Architecture](#-system-architecture) •
[Tech Stack](#️-technologies-used) •
[Installation](#-installation) •
[Usage](#-processing-pipeline)

</p>

---

# 🎯 Overview

**AI News Generator** is an intelligent **Multi-Agent AI system** that automatically transforms any topic into a complete news package consisting of a professionally written news article and an AI-generated realistic illustration.

The system collaborates through multiple specialized AI agents that perform web searching, article extraction, relevance evaluation, summarization, article writing, prompt engineering, and image generation, all within a single interactive Streamlit application.

Unlike traditional text generators, this project integrates **information retrieval, content synthesis, and generative AI** into a unified workflow, producing informative and visually engaging news content with minimal user input.

---

# ✨ Key Features

- 🌐 Automated web search using DuckDuckGo Search (DDGS)
- 📄 Intelligent extraction of article content from multiple sources
- 🧹 Duplicate URL removal and content preprocessing
- 🎯 AI-powered relevance evaluation for filtering useful articles
- 📝 Structured summarization of extracted news sources
- 📰 Professional article generation using a Large Language Model
- 🎨 Automatic scene understanding and image prompt generation
- 🖼️ Realistic news illustration generation using RealVisXL
- 📊 Interactive Streamlit dashboard with real-time pipeline progress
- 💾 Automatic storage of intermediate and final outputs in JSON and Markdown formats

---

# 🏗️ System Architecture

The project follows a **Multi-Agent Architecture**, where each agent is responsible for a dedicated task within the news generation pipeline.

```
                    User Topic
                         │
                         ▼
              Search Query Generation
                         │
                         ▼
               DuckDuckGo Search (DDGS)
                         │
                         ▼
              Duplicate URL Filtering
                         │
                         ▼
             Article Content Extraction
                         │
                         ▼
              AI Relevance Evaluation
                         │
                         ▼
             News Source Summarization
                         │
                         ▼
            Professional Article Writing
                         │
                         ▼
           Scene Detection & Prompt Creation
                         │
                         ▼
         RealVisXL Image Generation Model
                         │
                         ▼
              Streamlit User Interface
```

---

# 🤖 Multi-Agent Workflow

## 🔍 Search Agent

Responsible for:

- Generating effective search queries
- Searching multiple news sources using DDGS
- Collecting relevant URLs
- Removing duplicate links
- Extracting raw article content

**Output**

```
data/extracted_articles.json
```

---

## 📑 Summary Agent

Responsible for:

- Reading extracted news articles
- Evaluating source relevance
- Removing unrelated content
- Creating structured summaries
- Preserving important entities and facts

**Output**

```
data/source_summaries.json
```

---

## 📰 Article Agent

Responsible for:

- Combining multiple source summaries
- Generating a coherent news article
- Maintaining journalistic writing style
- Producing a complete Markdown article

**Output**

```
outputs/articles/final_article.md
```

---

## 🎨 Image Agent

Responsible for:

- Reading the generated article
- Detecting the primary event
- Identifying important objects, people, and locations
- Creating a detailed image generation prompt
- Generating a realistic illustration using RealVisXL

**Output**

```
outputs/images/final_news_image.png
```

---

# 📂 Project Structure

```
AI-News-Generator/
│
├── agents/
│   ├── search_agent.py
│   ├── summary_agent.py
│   ├── article_agent.py
│   └── image_agent.py
│
├── assets/
│
├── data/
│   ├── extracted_articles.json
│   └── source_summaries.json
│
├── logs/
│
├── outputs/
│   ├── articles/
│   └── images/
│
├── utils/
│
├── .env
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Technologies Used

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3.9+ |
| User Interface | Streamlit |
| Web Search | DuckDuckGo Search (DDGS) |
| Content Extraction | Trafilatura |
| Large Language Model | Groq API |
| Image Generation | RealVisXL |
| Data Storage | JSON |
| Configuration | python-dotenv |
| Version Control | Git & GitHub |

---

# 🚀 Processing Pipeline

The application follows the workflow below:

1. User enters a news topic.
2. Search Agent generates optimized search queries.
3. DDGS retrieves related news articles.
4. Duplicate URLs are removed.
5. Article content is extracted.
6. AI evaluates article relevance.
7. Relevant articles are summarized.
8. Article Agent creates a professional news report.
9. Image Agent generates a detailed visual prompt.
10. RealVisXL creates a realistic news illustration.
11. Results are displayed in the Streamlit dashboard.

---

# 📊 Generated Outputs

The application produces multiple outputs throughout the pipeline.

### Intermediate Files

- Extracted Articles
- Source Summaries

### Final Outputs

- Professional News Article (Markdown)
- AI-generated News Illustration (PNG)

---

# 💻 Streamlit Dashboard

The interactive dashboard provides:

- Topic input interface
- Real-time pipeline progress
- Generated news article
- AI-generated illustration
- Intermediate processing status
- Downloadable outputs

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# 🚀 Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/AI-News-Generator.git
```

Move into the project directory.

```bash
cd AI-News-Generator
```

Install all dependencies.

```bash
pip install -r requirements.txt
```

Configure your environment variables.

```bash
GROQ_API_KEY=your_api_key
```

Run the application.

```bash
streamlit run app.py
```

---

# 🎯 Use Cases

- Automated news generation
- AI-assisted journalism
- News summarization
- Information aggregation
- Educational demonstrations of multi-agent AI systems
- Research on AI-powered content generation

---

# 🔮 Future Improvements

- Support for multiple LLM providers
- Multilingual news generation
- Real-time trending topic detection
- Source credibility scoring
- Multi-image generation
- Article fact verification
- Export to PDF and DOCX
- Audio news narration
- Cloud deployment

---





</p>
