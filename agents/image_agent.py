import os
import torch
from dotenv import load_dotenv
from diffusers import AutoPipelineForText2Image
from langchain_groq import ChatGroq

# ==========================================================
# Load Pipeline (Called Only Once)
# ==========================================================
def load_pipeline():

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"\nLoading Image Model on {device}...\n")

    pipe = AutoPipelineForText2Image.from_pretrained(
        "SG161222/RealVisXL_V5.0",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        variant="fp16",
        use_safetensors=True,
    )

    pipe = pipe.to(device)

    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()

    print("Image Model Loaded Successfully!\n")

    return pipe


# ==========================================================
# Generate Image
# ==========================================================
def generate_image(
    article,
    pipe,
    output_path="outputs/final_news_image.png"
):
    """
    Generate a realistic news image from an article.

    Parameters
    ----------
    article : str
        Final article.

    pipe :
        Already loaded Stable Diffusion pipeline.

    output_path : str
        Where image will be saved.

    Returns
    -------
    str
        Saved image path.
    """

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")

    # ======================================================
    # Initialize Groq
    # ======================================================
    client = ChatGroq(
        groq_api_key=api_key,
        model_name="openai/gpt-oss-120b",
        temperature=0.2,
    )

    print("\nGenerating Visual Prompt...\n")

    visual_prompt_request = f"""
You are an award-winning Reuters photo editor.

Read the article carefully.

Understand:

- Main event
- Most important moment
- Location
- Key people
- Objects
- Emotions
- Actions
- Environment

Generate ONE Stable Diffusion XL prompt.

Rules:

- One single realistic scene.
- No collages.
- No multiple panels.
- No portraits.
- No headshots.
- Show complete environment.
- Show realistic people.
- Reuters photojournalism.
- Documentary photography.
- Wide-angle composition.
- Natural lighting.
- High detail.
- Environmental storytelling.

Return ONLY the prompt.

Article:

{article}
"""

    visual_prompt = client.invoke(
        visual_prompt_request
    ).content.strip()

    print("=" * 80)
    print("VISUAL PROMPT")
    print("=" * 80)
    print(visual_prompt)

    print("\nGenerating Image...\n")

    image = pipe(
        prompt=visual_prompt,

        negative_prompt="""
cartoon,
anime,
painting,
illustration,
watermark,
logo,
text,
portrait,
headshot,
close-up,
blurry,
low quality,
duplicate,
bad anatomy,
cropped,
cgi
""",

        num_inference_steps=30,
        guidance_scale=7.5,
        width=1344,
        height=768,

    ).images[0]

    os.makedirs("outputs", exist_ok=True)

    image.save(output_path)

    print(f"\nImage Saved: {output_path}")

    return output_path