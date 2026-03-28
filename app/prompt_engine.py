import os
import json
import logging
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enhance_storyboard_prompts(sentences: list[str], style: str) -> list[str]:
    """
    Transforms a list of basic sentences into a visually rich, cinematic storyboard prompts.
    Uses Gemini to establish a global character/environment description to guarantee visual consistency.
    Returns a list of highly detailed prompts, one for each input sentence.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Falling back to rule-based prompt generation.")
        return [_fallback_prompt(sentence, style) for sentence in sentences]
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        system_instructions = (
            "You are an elite AI image prompt engineer. Your task is to process a sequence of narrative sentences "
            "and generate a meticulously detailed prompt for EACH sentence, perfectly optimized for an Image Generator like DALL-E 3.\n\n"
            "CRITICAL: To achieve VISUAL CONSISTENCY across the storyboard, you MUST first establish a 'Global Aesthetic & Character Design' "
            "based on the story. You MUST physically inject this exact global description (e.g. physical traits, clothing, environment palette) "
            "into every single individual prompt so the characters look definitively identical across scenes.\n\n"
            "Include specific, evocative details regarding: lighting, camera angle, atmosphere, and textural details based strictly on the requested style.\n\n"
            "You MUST return a pure JSON array of strings ONLY. The array length MUST exactly match the number of input sentences.\n"
            "Format: [\"prompt for scene 1\", \"prompt for scene 2\", ...]"
        )
        
        numbered_sentences = "\n".join([f"{i+1}. {s.strip()}" for i, s in enumerate(sentences)])
        
        user_input = f"Target Style: {style}\n\nStory Scenes:\n{numbered_sentences}"
        full_prompt = f"{system_instructions}\n\n{user_input}"
        
        response = model.generate_content(full_prompt)
        
        if response.text:
            try:
                prompts_array = json.loads(response.text)
                if isinstance(prompts_array, list) and len(prompts_array) == len(sentences):
                    logger.info("Successfully generated consistent storyboard prompts via Gemini.")
                    return prompts_array
                else:
                    logger.error("Gemini returned invalid JSON structure or mismatched length.")
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON array from Gemini.")
                
        raise ValueError("Invalid Gemini completion")
            
    except Exception as e:
        logger.error(f"Gemini storyboard prompt enhancement failed: {e}. Using fallback.")
        return [_fallback_prompt(sentence, style) for sentence in sentences]

def _fallback_prompt(sentence: str, style: str) -> str:
    """A highly structured rule-based fallback prompt."""
    return (
        f"A breathtaking, masterpiece artwork in the style of {style}. "
        f"Subject: {sentence.strip()}. "
        f"Execution: highly detailed, 8k resolution, visually stunning, intricate textures. "
        f"Lighting and Atmosphere: cinematic lighting, dynamic shadows, rich color grading, evocative mood. "
        f"Composition: professional cinematography, perfect framing."
    )
