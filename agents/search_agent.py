import os
import json
import time
from dotenv import load_dotenv
from ddgs import DDGS
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer, util
from utils import logger
from utils import constants

# Load embedding model for semantic relevance
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Trusted domains whitelist
TRUSTED_DOMAINS = {"bbc.com", "reuters.com", "nature.com", "openai.com"}

def generate_queries(topic):
    """
    Generate multiple context-aware queries for better relevance.
    """
    base = topic.lower()
    queries = [
        f"{base} latest news",
        f"{base} industry updates 2026",
        f"{base} research breakthroughs",
        f"{base} government policies",
        f"{base} site:bbc.com {base}",
        f"{base} site:reuters.com {base}",
        f"{base} site:nature.com {base}",
        f"{base} site:openai.com {base}"
    ]
    return queries


def run_search_agent(topic):
    """
    Search the web, extract content, filter by relevance,
    and save the summaries to source_summaries.json.
    """

    # =====================================
    # Load Environment Variables
    # =====================================
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    # =====================================
    # Initialize Groq
    # =====================================
    client = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    logger.info("=" * 80)
    logger.info(f"Searching for: {topic}")
    logger.info("=" * 80)

    # =====================================
    # Search and Extract Content
    # =====================================
    all_articles = []
    seen_urls = set()
    queries = generate_queries(topic)

    with DDGS() as ddgs:
        for q in queries:
            logger.info(f"\nQuery: {q}")
            try:
                search_results = ddgs.text(q, max_results=10)
            except Exception as e:
                logger.error(f"Search error for query '{q}': {e}")
                continue

            for result in search_results:
                try:
                    url = result.get("href")
                    title = result.get("title", "")
                    date = result.get("date", "")
                    domain = url.split("/")[2] if url else ""

                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)

                    # Enforce domain whitelist
                    if not any(d in domain for d in TRUSTED_DOMAINS):
                        logger.warning(f"Skipped non-whitelisted domain: {domain}")
                        continue

                    logger.info(f"Extracting: {url}")
                    article = ddgs.extract(url, fmt="text_markdown")
                    content = article.get("content", "")

                    if content:
                        all_articles.append({
                            "title": title,
                            "url": url,
                            "date": date,
                            "domain": domain,
                            "content": content
                        })
                        logger.info("Extracted Successfully")
                        logger.debug(content[:300])

                    time.sleep(1)  # rate limiting

                except Exception as e:
                    logger.error(f"Extraction Error: {e}")

    logger.info(f"\nTotal Extracted Sources: {len(all_articles)}")

    # =====================================
    # Relevance Filtering using embeddings
    # =====================================
    Final_summaries = []
    topic_embedding = embedder.encode(topic, convert_to_tensor=True)

    for idx, article in enumerate(all_articles):
        logger.info(f"\nProcessing Source {idx + 1}")

        content = article["content"][:5000]
        content_embedding = embedder.encode(content, convert_to_tensor=True)
        similarity = util.cos_sim(topic_embedding, content_embedding).item()

        if similarity < constants.RELEVANCE_THRESHOLD:  # configurable threshold
            logger.warning(f"Discarded (low relevance, score={similarity:.2f})")
            continue

        prompt = f"""
You are an expert research analyst.

Analyze the following content carefully.

Return ONLY valid JSON.

Required JSON Structure:
{{
    "summary":"150-word factual summary",
    "keywords":[],
    "entities":[],
    "date":"{article['date']}",
    "source":"{article['domain']}"
}}

Topic:
{topic}

Content:
{content}
"""

        try:
            response = client.invoke(prompt)
            cleaned_response = response.content.strip()
            cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()
            parsed_json = json.loads(cleaned_response)

            # Validate summary field
            if "summary" not in parsed_json or not parsed_json["summary"].strip():
                logger.error(f"Invalid summary for Source {idx + 1}")
                continue

            Final_summaries.append({
                "source_id": idx + 1,
                "title": article["title"],
                "url": article["url"],
                "parsed_content": parsed_json
            })

            logger.info(f"Source {idx + 1} Processed Successfully (score={similarity:.2f})")

        except Exception as e:
            logger.error(f"Error in Source {idx + 1}: {e}")

    # =====================================
    # Save JSON
    # =====================================
    os.makedirs("data", exist_ok=True)
    output_path = "data/source_summaries.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(Final_summaries, f, indent=4, ensure_ascii=False)

    logger.info("\nSource summaries saved successfully!")
    logger.info(output_path)

    return output_path
