import os
import uuid
import logging
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)

def generate_image(prompt: str) -> str:
    """
    Generates an image using OpenAI's DALL-E model.
    Saves the image locally and returns the relative path.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable is missing.")
        return "https://placehold.co/1024x1024/EEE/31343C?text=API+Key+Missing"
        
    try:
        client = OpenAI(api_key=api_key)
        
        # Let the user know the log in case of UI delays
        logger.info(f"Generating image with DALL-E for prompt: {prompt[:50]}...")
        
        # Make the request to OpenAI
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt[:1000],  # DALL-E 3 supports up to 4000 chars, this is an arbitrary cutoff limit just to be safe
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        if not image_url:
            raise Exception("No image URL returned from OpenAI")
            
        # Download the image
        img_data = requests.get(image_url).content
        filename = f"{uuid.uuid4().hex}.png"
        
        # Save path relative to application root
        save_dir = os.path.join("static", "generated_images")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        
        with open(save_path, 'wb') as handler:
            handler.write(img_data)
            
        return f"generated_images/{filename}"
    except Exception as e:
        logger.error(f"Error generating image with OpenAI: {e}")
        # Return fallback error placeholder
        return "https://placehold.co/1024x1024/EEE/31343C?text=Image+Generation+Failed"
