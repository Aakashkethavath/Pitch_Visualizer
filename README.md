# Pitch Visualizer

A production-ready web application that transforms narrative text into a stunning, multi-panel AI-generated storyboard. It leverages advanced Large Language Models for prompt engineering and DALL-E 3 for high-fidelity image generation.

## Features
- **Dynamic UI Streaming**: Watch your storyboard build itself in real-time. Panels cleanly animate onto the page the exact millisecond they finish generating using JSON Lines streaming!
- **Visual Consistency Engine**: Uses Google Gemini to analyze the *entire* story at once. It establishes a "Global Aesthetic & Character Design" ruleset and physically injects it into every single scene's prompt, elegantly guaranteeing characters look identical across all panels.
- **Narrative Text Segmentation**: Intelligently splits paragraphs into cinematic scenes using Natural Language Processing (NLTK).
- **Pro-Level Prompt Engineering**: Translates mundane sentences into meticulously detailed, professional image generation prompts using Gemini 2.5 Flash.
- **User-Selectable Styles**: Choose your artistic direction before generating (Realistic, Cartoon, Anime, Sci-Fi Concept Art).

## Tech Stack
- **Backend Architecture**: Python, Flask, Server-Sent Events (SSE) / JSON Lines
- **Frontend**: HTML5, Vanilla JavaScript (ReadableStreams API), Tailwind CSS
- **NLP Text Splicing**: NLTK (`sent_tokenize`)
- **AI Prompt Engineering**: Google Gemini (`google-generativeai`)
- **Image Generation Pipeline**: OpenAI DALL-E 3 (`openai`)

## Setup Instructions

### 1. Requirements
Ensure you have Python 3.9+ installed, along with valid API keys for both Google Gemini and OpenAI.

### 2. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install Dependencies
Create a virtual environment:
```bash
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate
```

Install the library dependencies:
```bash
pip install -r requirements.txt
```

### 4. Running the Application
Start the Flask development server:
```bash
python app/main.py
```

Open your browser to: `http://localhost:5000`

## Architecture Flow
1. **User Input Phase**: The user submits narrative text and an artistic style preference through the interactive frontend.
2. **Segmentation (`app/segmentation.py`)**: Utilizes NLTK to slice the narrative block into logical pacing beats and individual sentences.
3. **Consistency Enhancement (`app/prompt_engine.py`)**: Sits between the text and the Image Generator. Passes the entire array of scenes to Gemini to build a universal character context map, returning a JSON array of highly detailed, strictly consistent prompts.
4. **Generation (`app/image_generator.py`)**: Executes requests to OpenAI's DALL-E 3 API, downloading and saving the resulting images to the local `/static` directory.
5. **Real-Time Streaming (`app/storyboard.py` & `app/main.py`)**: Designed as a Python Generator function that constantly maintains an open HTTP connection to the browser, pushing chunks of JSON panel data the instant they are rendered.

## Design Choices & Prompt Engineering Methodology

Creating a seamless, visually consistent storyboard required several intentional design choices, specifically regarding how we interpret text and guide AI image generators.

### 1. Panel-by-Panel Streaming UI
**Choice:** Instead of blocking the client for 15-30+ seconds while generating 3-5 images server-side, the backend was designed as a Python Generator function.
**Reason:** By using Flask's `stream_with_context` paired with the browser's native `ReadableStreams` API, the application immediately delivers a generated image to the UI the exact second OpenAI finishes rendering it. This drastically improves perceived performance and UX.

### 2. Context-Aware Prompt Engineering
**Choice:** Using Gemini 2.5 Flash as an intermediate "Prompt Engineer" rather than passing raw user sentences to DALL-E.
**Reason:** DALL-E operates on a per-image basis and possesses no memory of previously generated characters. 
**Methodology:** 
- Instead of processing sentences independently, the application sends the *entire array* of story scenes to Gemini in a single prompt.
- Gemini is instructed via a strict System Prompt to first establish a **"Global Aesthetic & Character Design"** blueprint based on the narrative. 
- It then mechanically injects these rigid character descriptions (e.g., specific clothing, hair color, environment details) and cinematic lighting techniques (e.g., volumetric lighting, Dutch angles) heavily into a returned JSON array of highly structured prompts.
- This enforces character consistency across independent API calls, effectively solving a classic challenge in generic AI generation.

### 3. Separation of Concerns
**Choice:** Modularity across the backend services (`segmentation.py`, `prompt_engine.py`, `image_generator.py`, `storyboard.py`).
**Reason:** This allows us to hot-swap technologies with minimal friction. For example, replacing local NLTK segmentation with an LLM, or swapping DALL-E 3 for Midjourney API or a local Stable Diffusion deployment, requires changes in only a single, isolated file.
