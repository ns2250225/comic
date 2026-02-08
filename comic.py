import requests
import base64

# ========== 配置 ==========
API_KEY = "sk-dwI0wRUeibzNWZYMDeA400D567354d85BdF3A8BfCeBc0aD3"
API_URL = "https://api.laozhang.ai/v1beta/models/gemini-3-pro-image-preview:generateContent"
PROMPT = "每一页漫画的提示词"
ASPECT_RATIO = "9:16"
IMAGE_SIZE = "2K"  # Nano Banana Pro 支持: 1K, 2K, 4K
# ============================

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": ASPECT_RATIO,
            "imageSize": IMAGE_SIZE
        }
    }
}

response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
result = response.json()

# 保存图片
image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
with open("output.png", "wb") as f:
    f.write(base64.b64decode(image_data))

print("✅ 图片已保存: output.png")