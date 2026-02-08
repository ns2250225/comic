from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import StoryRequest, ImageRequest
from api import generate_story_logic, generate_image_logic
import uvicorn

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "*" # For development simplicity
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/story")
async def generate_story(request: StoryRequest):
    data = generate_story_logic(request.character, request.plot, request.page_count)
    # Ensure structure matches StoryResponse if possible, or just return dict
    # The API returns: {"title": "...", "pages": [{"prompt": "...", ...}, ...]}
    # We might need to map it if the structure varies, but let's assume the LLM follows instructions.
    return data

@app.post("/api/image")
async def generate_image(request: ImageRequest):
    # Combine character design with page prompt to ensure consistency
    full_prompt = request.prompt
    if request.character_design:
        full_prompt = f"Character Design: {request.character_design}. \n\n" + full_prompt
        
    image_base64 = generate_image_logic(full_prompt)
    return {"image_data": image_base64}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
