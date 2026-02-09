# ComicGen 🎨

ComicGen 是一个 AI 驱动的漫画生成平台，可以将文本故事转化为视觉化的漫画页面。它利用大语言模型（LLM）进行故事板创作和角色一致性控制，并使用图像生成模型创作高质量的漫画分格。

## 功能特性 ✨

-   **AI 故事生成**：输入角色和情节，即可生成包含详细场景、镜头和对白描述的多页漫画脚本。
-   **角色一致性**：自动生成并锁定角色设计，确保主角在所有画面中的形象保持一致。
-   **多格页面生成**：生成包含 4-5 个分格的完整漫画页面。
-   **交互式 UI**：基于 Vue 3 和 Tailwind CSS 构建的现代化分屏界面。
-   **批量下载**：支持将整部漫画下载为 ZIP 文件。

## 界面预览
![](./demo.jpeg)


## 技术栈 🛠️

-   **前端**：Vue 3, Vite, Tailwind CSS, Axios
-   **后端**：FastAPI, Python 3.10
-   **AI 集成**：OpenAI SDK (兼容 DeepSeek/Gemini API)
-   **容器化**：Docker, Docker Compose

##先决条件 📋

-   [Docker](https://www.docker.com/get-started) 和 [Docker Compose](https://docs.docker.com/compose/install/)
-   **或者** 进行本地非 Docker 设置：
    -   Node.js (v18+)
    -   Python (v3.10+)

## 快速开始 (Docker) 🐳

1.  **克隆仓库** (如果适用) 或导航到项目根目录。

2.  **使用 Docker Compose 运行**：
    ```bash
    docker-compose up --build
    ```

3.  **访问应用**：
    -   前端：[http://localhost:5173](http://localhost:5173)
    -   后端 API：[http://localhost:8000/docs](http://localhost:8000/docs)

## 本地开发设置 💻

### 后端

1.  进入 `backend` 目录：
    ```bash
    cd backend
    ```

2.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

3.  运行服务器：
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### 前端

1.  进入 `frontend` 目录：
    ```bash
    cd frontend
    ```

2.  安装依赖：
    ```bash
    npm install
    ```

3.  运行开发服务器：
    ```bash
    npm run dev
    ```

4.  访问 `http://localhost:5173` (或终端显示的端口)。

## 环境变量 🔑

为了演示目的，当前应用在 `backend/api.py` 中使用了硬编码的 API 密钥。在生产环境中，您应该将其替换为环境变量：

-   `API_KEY`：您的 LLM 和图像生成服务 API 密钥。
-   `BASE_URL_TEXT`：文本生成 API 的基础 URL。
-   `BASE_URL_IMAGE`：图像生成 API 的 URL。

## 项目结构 📂

```
comic/
├── backend/                # FastAPI 后端
│   ├── Dockerfile
│   ├── api.py              # 外部 API 调用逻辑
│   ├── main.py             # 应用入口点
│   ├── models.py           # Pydantic 模型
│   └── requirements.txt
├── frontend/               # Vue 3 前端
│   ├── Dockerfile
│   ├── nginx.conf          # Docker 的 Nginx 配置
│   ├── src/                # Vue 源代码
│   └── ...
├── docker-compose.yml      # Docker 编排文件
└── README.md               # 项目文档
```

## 许可证 📄

[MIT](LICENSE)
