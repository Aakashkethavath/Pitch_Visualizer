import json
from app.segmentation import segment_text
from app.prompt_engine import enhance_storyboard_prompts
from app.image_generator import generate_image

def create_storyboard_stream(text: str, style: str):
    """
    Generator that parses text, generates prompts holistically for consistency, 
    and yields individual storyboard panels once their images are ready.
    """
    segments = segment_text(text)
    
    # Generate all prompts at once to ensure character/style consistency
    enhanced_prompts = enhance_storyboard_prompts(segments, style)
    
    # Iterate through each scene, generate the image, and immediately yield it
    for segment, enhanced_prompt in zip(segments, enhanced_prompts):
        try:
            image_path = generate_image(enhanced_prompt)
            
            # Ensure proper URL formatting for static files vs absolute URLs
            image_url = image_path if image_path.startswith("http") else f"/static/{image_path}"
            
            panel_data = {
                "original_text": segment,
                "enhanced_prompt": enhanced_prompt,
                "image_url": image_url
            }
            
            # Yield as a JSON string formatted for HTTP chunks in application/jsonl format
            yield json.dumps(panel_data) + "\n"
        except Exception as e:
            error_msg = str(e).lower()
            if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg or "429" in error_msg:
                user_msg = "Image Generation Failed: OpenAI API credits are 0 or quota exceeded. Please check your billing details."
            else:
                user_msg = f"Image Generation Failed: {str(e)}"
                
            panel_data = {
                "error": user_msg
            }
            yield json.dumps(panel_data) + "\n"
            break  # Stop processing further scenes if an error occurs

