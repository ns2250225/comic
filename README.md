# ComicGen 🎨

ComicGen is an AI-powered comic generation platform that transforms text stories into visual comic pages. It uses Large Language Models (LLM) for storyboarding and character consistency, and Image Generation models for creating high-quality panels.

## Features ✨

-   **AI Story Generation**: Input a character and plot to generate a multi-page comic script with detailed scene, shot, and dialogue descriptions.
-   **Character Consistency**: Automatically generates and locks a character design to ensure the protagonist looks the same across all panels.
-   **Multi-Panel Page Generation**: Generates full comic pages containing 4-5 panels each.
-   **Interactive UI**: Modern, split-screen interface built with Vue 3 and Tailwind CSS.
-   **Batch Download**: Download the entire comic as a ZIP file.

## Tech Stack 🛠️

-   **Frontend**: Vue 3, Vite, Tailwind CSS, Axios
-   **Backend**: FastAPI, Python 3.10
-   **AI Integration**: OpenAI SDK (compatible with DeepSeek/Gemini APIs)
-   **Containerization**: Docker, Docker Compose

## Prerequisites 📋

-   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
-   **Or** for local non-Docker setup:
    -   Node.js (v18+)
    -   Python (v3.10+)

## Quick Start (Docker) 🐳

1.  **Clone the repository** (if applicable) or navigate to the project root.

2.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the application**:
    -   Frontend: [http://localhost:5173](http://localhost:5173)
    -   Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development Setup 💻

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the server:
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

4.  Access at `http://localhost:5174` (or port shown in terminal).

## Environment Variables 🔑

The application currently uses hardcoded API keys for demonstration purposes in `backend/api.py`. For a production environment, you should replace these with environment variables:

-   `API_KEY`: Your API key for the LLM and Image Generation service.
-   `BASE_URL_TEXT`: Base URL for the text generation API.
-   `BASE_URL_IMAGE`: URL for the image generation API.

## Project Structure 📂

```
comic/
├── backend/                # FastAPI backend
│   ├── Dockerfile
│   ├── api.py              # Logic for external API calls
│   ├── main.py             # App entry point
│   ├── models.py           # Pydantic models
│   └── requirements.txt
├── frontend/               # Vue 3 frontend
│   ├── Dockerfile
│   ├── nginx.conf          # Nginx config for Docker
│   ├── src/                # Vue source code
│   └── ...
├── docker-compose.yml      # Docker composition
└── README.md               # Project documentation
```

## License 📄

[MIT](LICENSE)
