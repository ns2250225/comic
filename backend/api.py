import json
import requests
import base64
import os
import time
from openai import OpenAI
from fastapi import HTTPException

# Configuration
API_KEY = "sk-dwI0wRUeibzNWZYMDeA400D567354d85BdF3A8BfCeBc0aD3"
BASE_URL_TEXT = "https://api.laozhang.ai/v1"
BASE_URL_IMAGE = "https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL_TEXT
)

def generate_story_logic(character: str, plot: str, page_count: int = 3):
    prompt = f"设计一个多页彩色分格漫画，对话使用中文，主角为【{character}】的角色，你要定义一个【{plot}】的情节。请首先设计主角的详细视觉形象（包括发型、发色、服装、配饰等），然后设计{page_count}页漫画，每一页包含4-5个分格（Panels）。要求详细描述每一格的画面内容、景别、镜头和对白。请直接返回JSON格式，不要包含markdown代码块标记。"
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": """请直接返回JSON格式，不要包含markdown代码块标记。
返回格式示例：
{
  "title": "漫画标题",
  "character_design": "主角的详细视觉描述，例如：一个穿着红色连帽衫的短发小男孩，背着蓝色书包，眼神坚毅。",
  "pages": [
    {
      "page_number": 1,
      "panels": [
        {
          "panel_number": 1,
          "text": "画面描述内容",
          "dialogue": "角色对白",
          "scene": "景别（如：全景）",
          "shot": "镜头（如：俯视）"
        },
        ...
      ]
    },
    ...
  ]
}"""},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        print(f"DEBUG: Raw LLM Response: {content}") # Debug print
        
        # Clean up if there are markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        data = json.loads(content)
        print(f"DEBUG: Parsed JSON: {data}") # Debug print
        
        # Parse and normalize data
        normalized_data = {"title": "Comic Story", "character_design": "", "pages": []}
        
        if "title" in data:
            normalized_data["title"] = data["title"]
        elif "漫画标题" in data:
            normalized_data["title"] = data["漫画标题"]
            
        if "character_design" in data:
            normalized_data["character_design"] = data["character_design"]
        elif "角色形象" in data:
            normalized_data["character_design"] = data["角色形象"]
        elif "角色设定" in data:
             normalized_data["character_design"] = data["角色设定"]
            
        raw_pages = []
        if "pages" in data:
            raw_pages = data["pages"]
        elif "页面结构" in data:
            raw_pages = data["页面结构"]
            
        mapped_pages = []
        for i, page in enumerate(raw_pages):
            panels_data = page.get("panels", [])
            if not panels_data and "画面详情" in page:
                panels_data = page["画面详情"]
            
            mapped_panels = []
            page_prompt_parts = []
            
            for j, panel in enumerate(panels_data):
                text = panel.get("text") or panel.get("内容") or panel.get("prompt") or ""
                scene = panel.get("scene") or panel.get("景别")
                shot = panel.get("shot") or panel.get("镜头")
                dialogue = panel.get("dialogue") or panel.get("对白")
                
                # Construct individual panel prompt part
                panel_desc = f"Panel {j+1}: {text}"
                if scene: panel_desc += f", {scene}"
                if shot: panel_desc += f", {shot}"
                if dialogue: panel_desc += f", Dialogue: '{dialogue}'"
                
                page_prompt_parts.append(panel_desc)
                
                mapped_panels.append({
                    "panel_number": j + 1,
                    "text": text,
                    "scene": scene,
                    "shot": shot,
                    "dialogue": dialogue
                })
            
            # Construct the full page prompt
            full_page_prompt = f"A comic page with {len(mapped_panels)} panels. " + " ".join(page_prompt_parts) + ". Style: Colorful, Detailed, Comic Book Style."
            
            mapped_pages.append({
                "page_number": i + 1,
                "panels": mapped_panels,
                "prompt": full_page_prompt,
                "status": "pending"
            })
            
        normalized_data["pages"] = mapped_pages
        return normalized_data

    except Exception as e:
        print(f"Error generating story: {e}")
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

def generate_image_logic(prompt: str):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": "9:16",
                "imageSize": "1K"
            }
        }
    }
    
    try:
        response = requests.post(BASE_URL_IMAGE, headers=headers, json=payload, timeout=180)
        response.raise_for_status()
        result = response.json()
        
        image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        return image_data # Returns base64 string
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
