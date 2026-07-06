import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from ddgs import DDGS

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY not found in .env")

# ==========================
# Initialize Groq
# ==========================
client = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.3,
)

# ==========================
# User Input
# ==========================
topic = input("\nEnter Topic: ").strip()

print("\n" + "=" * 80)
print("TOPIC:", topic)
print("=" * 80)

# Generate Better Search Queries

query_prompt = f"""
You are a research expert.

Generate 5 highly effective Google search queries for the topic.

Topic:
{topic}

Rules:
- Cover different aspects
- Recent information
- Research studies
- Industry reports
- Expert opinions

Output only the queries.
One query per line.
"""

response = client.invoke(query_prompt)

queries = [
    q.strip().lstrip("1234567890.- ")
    for q in response.content.split("\n")
    if q.strip()
]

print("\nGenerated Queries:\n")

for q in queries:
    print("•", q)


# Search Web

all_urls = set()

with DDGS() as ddgs:

    for query in queries:

        print(f"\nSearching: {query}")

        try:

            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )

            for result in results:

                url = (
                    result.get("href")
                    or result.get("url")
                    or result.get("link")
                )

                if url:
                    all_urls.add(url)

        except Exception as e:
            print("Search Error:", e)

# ==========================
# Keep Top 20 Links
# ==========================
top_links = list(all_urls)[:20]

print("\n" + "=" * 80)
print("TOP 20 LINKS")
print("=" * 80)

for i, link in enumerate(top_links, start=1):
    print(f"{i}. {link}")

# ==========================
# Save Links
# ==========================
# with open("sources.txt", "w", encoding="utf-8") as f:

#     for i, link in enumerate(top_links, start=1):
#         f.write(f"{i}. {link}\n")

# print("\n✓ Top 20 links saved to sources.txt")