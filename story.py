from openai import OpenAI

client = OpenAI(
    api_key="sk-dwI0wRUeibzNWZYMDeA400D567354d85BdF3A8BfCeBc0aD3",
    base_url="https://api.laozhang.ai/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "设计一个多页彩色分格漫画，对话使用中文，主角为【用户填写的角色文本】的角色，你要定义一个【用户填写的故事情节】的情节，并且细化漫画每一格的具体内容，要包括“景别”，“内容”，“对白”，“镜头”等。要求返回包含漫画的标题和每一页的画面提示词的json数据。"}
    ]
)

print(response.choices[0].message.content)