import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq


def generate_article(summary_file="data/source_summaries.json"):
    """
    Reads source summaries from JSON,
    generates the final news article,
    saves it as Markdown,
    and returns the article text.
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
        model_name="llama-3.1-8b-instant",
        temperature=0.3,
    )

    # =====================================
    # Read Source Summaries
    # =====================================
    with open(summary_file, "r", encoding="utf-8") as f:
        summaries = json.load(f)

    print("=" * 80)
    print("Generating Final Article...")
    print("=" * 80)

    # =====================================
    # Combine All Summaries
    # =====================================
    combined_summary = ""

    for source in summaries:

        summary = source["parsed_content"]["summary"]

        combined_summary += summary + "\n\n"

    print("Total Summary Length :", len(combined_summary))

    # Prevent token overflow
    combined_summary = combined_summary[:15000]

    # =====================================
    # Prompt
    # =====================================
    prompt = f"""
You are a journalist and professional news editor working for a globally recognized news agency.

Your responsibility is to transform the provided summaries into a publication-ready news article.

Instructions:

- Carefully analyze all summaries before writing.
- Generate one informative and engaging main headline.
- Organize the article into 3–4 sections.
- Give each section a meaningful subheading.
- Write detailed paragraphs under every subheading.

The article should clearly answer:

1. What happened?
2. Where did it happen?
3. When did it happen?
4. Who was involved?
5. Why is it important?

Preserve every important factual detail including:

- People
- Organizations
- Dates
- Locations
- Statistics
- Timelines

Do NOT:

- Add imaginary information.
- Remove important facts.
- Change statistics.
- Give opinions.
- Use informal language.
- Use abusive language.
- Use clickbait.

Maintain:

- Neutral tone
- Professional journalism
- Guardian-style writing
- Clear readability

Write approximately 500 words.

Source Summaries:

{combined_summary}
"""

    # =====================================
    # Generate Article
    # =====================================
    response = client.invoke(prompt)

    article = response.content

    # =====================================
    # Create data folder
    # =====================================
    os.makedirs("data", exist_ok=True)

    article_path = "data/final_article.md"

    # =====================================
    # Save Markdown
    # =====================================
    with open(
        article_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(article)

    print("\nFinal Article Saved Successfully!")
    print(article_path)

    return article