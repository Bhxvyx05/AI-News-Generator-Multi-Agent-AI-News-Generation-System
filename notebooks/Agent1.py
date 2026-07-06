# # from hashlib import md5

# from diffusers import AutoPipelineForText2Image
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# # from markdown_it import MarkdownIt
# import torch
# import json
# import os

# # =====================================
# # Load Environment Variables
# # =====================================
# load_dotenv()

# # =====================================
# # Create Output Folder
# # =====================================
# os.makedirs("outputs", exist_ok=True)

# # =====================================
# # Initialize Groq
# # =====================================
# client = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"),
#     model_name="openai/gpt-oss-120b",
#     temperature=0.3,
#     # WE CAN ALSO USE 20b for the model_name, but 120b is more powerful and can handle complex queries better.
# )
# article = """Breaking News: Global Leaders Gather to Address Climate Change at Crucial Summit

# The world witnessed a historic gathering of global leaders as they convened to address the pressing issue of climate change at a crucial summit held in Paris, France. The highly anticipated event, which took place from November 1 to 12, 2021, brought together representatives from over 190 countries, including notable figures such as United States President Joe Biden, European Commission President Ursula von der Leyen, and Chinese Premier Xi Jinping. The primary objective of the summit was to discuss and implement concrete measures to mitigate the effects of climate change, which has become a pressing concern globally. As the world grapples with rising temperatures, devastating natural disasters, and unpredictable weather patterns, the summit aimed to provide a platform for nations to come together and pledge their commitment to reducing greenhouse gas emissions and transitioning to renewable energy sources.

# **Background and Context**
# The summit was a follow-up to the landmark Paris Agreement signed in 2015, which saw countries pledge to limit global warming to well below 2 degrees Celsius and pursue efforts to limit it to 1.5 degrees Celsius above pre-industrial levels. However, despite the initial enthusiasm and commitment, progress has been slow, and the world is still far from achieving the agreed-upon targets. The recent summit aimed to reinvigorate the global response to climate change, with a focus on increasing ambition, enhancing cooperation, and mobilizing finance to support developing countries in their transition to a low-carbon economy. According to the United Nations, the past decade was the warmest on record, with 2020 being the hottest year ever recorded, highlighting the urgent need for collective action to address the climate crisis.

# **Key Developments and Outcomes**
# The summit saw several key developments, including the launch of a new initiative to reduce methane emissions, a commitment by major economies to end deforestation by 2030, and a pledge by developed countries to mobilize $100 billion in climate finance per year by 2025. Additionally, the European Union announced plans to become carbon neutral by 2050, while China pledged to peak its carbon emissions before 2030. The summit also witnessed the signing of several bilateral agreements, including a deal between the United States and China to cooperate on climate change, marking a significant shift in the relationship between the two global powers. Despite these positive developments, critics argue that the summit did not go far enough, with some countries failing to submit updated national climate plans, and others resisting calls to phase out fossil fuels.

# **Significance and Future Implications**
# The outcome of the summit has significant implications for the future of the planet, as the world struggles to balance economic growth with environmental sustainability. The commitments made by global leaders will have far-reaching consequences, from shaping national energy policies to influencing international trade agreements. As the world moves forward, it is essential to ensure that the pledges made at the summit are translated into concrete actions, with countries held accountable for their progress. The success of the summit will be measured by the ability of nations to work together, share knowledge, and mobilize resources to address the climate crisis, which has become a defining issue of our time. With the next summit scheduled to take place in 2025, the world will be watching closely to see if the momentum generated in Paris can be sustained, and if the global community can come together to address the most pressing challenge of our era."""
# # =====================================
# # Load Story JSON
# # =====================================
# # with open("final_article.md", "r", encoding="utf-8") as f:
# #      data = MarkdownIt.markdown(f.read())


# # =====================================
# # Device Selection
# # =====================================
# device = "cuda" if torch.cuda.is_available() else "cpu"

# print(f"\nUsing Device: {device}")

# # =====================================
# # Load RealVisXL
# # =====================================
# pipe = AutoPipelineForText2Image.from_pretrained(
#     "SG161222/RealVisXL_V5.0",
#     torch_dtype=torch.float16 if device == "cuda" else torch.float32,
#     variant="fp16",
#     use_safetensors=True
# )

# pipe = pipe.to(device)

# print("Model Loaded Successfully!\n")

# # =====================================
# # Generate Images
# # =====================================
# # for point in data["points"]:

# #     story_id = point["id"]
# #     story_text = point["story"][:4000]

# #     print(f"\nProcessing Story ID: {story_id}")
# for article in article:
#     story_text = article

#     # =====================================
#     # Step 1: Convert Article -> Visual Prompt
#     # =====================================
#     prompt_generation = f"""
# You are a professional visual journalist.

# Read the news article and identify:

# - Main event
# - Location
# - Key people
# - Important actions
# - Environment
# - Emotions
# - Objects involved

# Generate ONE detailed image generation prompt.

# Rules:

# - Create a single scene.
# - Show the most important moment.
# - Show realistic actions.
# - Show realistic environment.
# - Show context of the event.
# - No collages.
# - No multiple panels.
# - No portraits.
# - No headshots.

# Style:

# Reuters photojournalism,
# documentary photography,
# realistic people,
# wide-angle shot,
# natural lighting,
# high detail,
# news photography.

# Article:

# {story_text}

# Output ONLY the final visual scene description.
# """

#     visual_prompt = client.invoke(prompt_generation).content

#     print("\nGenerated Visual Prompt:\n")
#     print(visual_prompt)

#     # =====================================
#     # Step 2: Generate Image
#     # =====================================
#     image = pipe(
#         prompt=visual_prompt,
#         negative_prompt="""
#         collage,
#         grid,
#         multiple panels,
#         portrait,
#         headshot,
#         close-up face,
#         cartoon,
#         anime,
#         painting,
#         illustration,
#         blurry,
#         low quality,
#         watermark,
#         text,
#         logo,
#         duplicate people,
#         deformed face
#         """,
#         num_inference_steps=30,
#         guidance_scale=7.5,
#         width=1344,
#         height=768
#     ).images[0]

#     # image_path = f"outputs/{story_id}.png"

#     # image.save(image_path)

#     # print(f"Saved: {image_path}")

# print("\nAll Images Generated Successfully!")


import os
import torch
from dotenv import load_dotenv
from diffusers import AutoPipelineForText2Image
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")


os.makedirs("outputs", exist_ok=True)


client = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="openai/gpt-oss-120b",
    temperature=0.2,
)


article = """
**Breaking News: Global Leaders Gather to Address Climate Change at Crucial Summit**

The world witnessed a historic gathering of global leaders as they convened to address the pressing issue of climate change at a crucial summit held in Paris, France. The highly anticipated event, which took place from November 1 to 12, 2021, brought together representatives from over 190 countries, including notable figures such as United States President Joe Biden, European Commission President Ursula von der Leyen, and Chinese Premier Xi Jinping. The primary objective of the summit was to discuss and implement concrete measures to mitigate the effects of climate change, which has become a pressing concern globally. As the world grapples with rising temperatures, devastating natural disasters, and unpredictable weather patterns, the summit aimed to provide a platform for nations to come together and pledge their commitment to reducing greenhouse gas emissions and transitioning to renewable energy sources.

**Background and Context**
The summit was a follow-up to the landmark Paris Agreement signed in 2015, which saw countries pledge to limit global warming to well below 2 degrees Celsius and pursue efforts to limit it to 1.5 degrees Celsius above pre-industrial levels. However, despite the initial enthusiasm and commitment, progress has been slow, and the world is still far from achieving the agreed-upon targets. The recent summit aimed to reinvigorate the global response to climate change, with a focus on increasing ambition, enhancing cooperation, and mobilizing finance to support developing countries in their transition to a low-carbon economy. According to the United Nations, the past decade was the warmest on record, with 2020 being the hottest year ever recorded, highlighting the urgent need for collective action to address the climate crisis.

**Key Developments and Outcomes**
The summit saw several key developments, including the launch of a new initiative to reduce methane emissions, a commitment by major economies to end deforestation by 2030, and a pledge by developed countries to mobilize $100 billion in climate finance per year by 2025. Additionally, the European Union announced plans to become carbon neutral by 2050, while China pledged to peak its carbon emissions before 2030. The summit also witnessed the signing of several bilateral agreements, including a deal between the United States and China to cooperate on climate change, marking a significant shift in the relationship between the two global powers. Despite these positive developments, critics argue that the summit did not go far enough, with some countries failing to submit updated national climate plans, and others resisting calls to phase out fossil fuels.

**Significance and Future Implications**
The outcome of the summit has significant implications for the future of the planet, as the world struggles to balance economic growth with environmental sustainability. The commitments made by global leaders will have far-reaching consequences, from shaping national energy policies to influencing international trade agreements. As the world moves forward, it is essential to ensure that the pledges made at the summit are translated into concrete actions, with countries held accountable for their progress. The success of the summit will be measured by the ability of nations to work together, share knowledge, and mobilize resources to address the climate crisis, which has become a defining issue of our time. With the next summit scheduled to take place in 2025, the world will be watching closely to see if the momentum generated in Paris can be sustained, and if the global community can come together to address the most pressing challenge of our era.
"""

# From this code it is connected to the device
device = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 80)
print("Device :", device)

if device == "cuda":
    print("GPU :", torch.cuda.get_device_name(0))

print("=" * 80)

# Load RealVisXL

print("\nLoading Image Model...\n")

pipe = AutoPipelineForText2Image.from_pretrained(
    "SG161222/RealVisXL_V5.0",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    variant="fp16",
    use_safetensors=True
)

pipe = pipe.to(device)

# Reduce VRAM usage
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

print("Model Loaded Successfully!")

# Generate Visual Prompt using Groq
print("\nGenerating Visual Prompt...\n")

prompt_generation = f"""
You are an award-winning Reuters photo editor and prompt engineer.

Read the following news article carefully.

Understand:

- the central event
- the most important moment
- the location
- the people involved
- their actions
- the surrounding environment
- important objects
- emotions
- atmosphere

Your task is to convert the article into ONE highly descriptive Stable Diffusion prompt.

Requirements:

- Focus on a single defining moment.
- Create one realistic news photograph.
- Show the complete environment instead of close-up faces.
- Include realistic human interactions.
- Mention architecture, weather, lighting, clothing, and important objects.
- Use cinematic composition.
- Use documentary photography style.
- Use Reuters-quality photojournalism.
- Highly realistic.
- Ultra detailed.
- Natural colors.
- Sharp focus.
- Environmental storytelling.

Return ONLY the image prompt.

Do not explain anything.

Do not use markdown.

Article:

{article}
"""

visual_prompt = client.invoke(prompt_generation).content.strip()

print("=" * 80)
print("VISUAL PROMPT")
print("=" * 80)
print(visual_prompt)

# Generate Image
print("\nGenerating Image...\n")

try:

    image = pipe(
        prompt=visual_prompt,
        negative_prompt="""
        cartoon,
        anime,
        painting,
        illustration,
        sketch,
        blurry,
        low quality,
        watermark,
        text,
        logo,
        duplicate,
        cropped,
        collage,
        multiple panels,
        portrait,
        headshot,
        close-up,
        deformed,
        bad anatomy,
        unrealistic,
        CGI,
        oversaturated,
        fake
        """,
        num_inference_steps=30,
        guidance_scale=7.5,
        width=1344,
        height=768,
    ).images[0]

    output_path = "outputs/final_news_image.png"

    image.save(output_path)

    print("\nImage Generated Successfully!")
    print(f"Saved at : {output_path}")

except Exception as e:

    print("\nImage Generation Failed!\n")
    print(e)