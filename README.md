# Papyro

A modern, lightweight, flat-file CMS built for speed and simplicity using FastAPI and Python.

## 🚀 Features

-   **Flat-file Storage**: No database required. Your content lives in Markdown files.
-   **FastAPI Powered**: High performance, async-first engine.
-   **Multi-Theming**: Switch between beautiful themes instantly.
-   **Dynamic Navigation**: Auto-generated menu based on your static pages.
-   **Live Reload**: Develop content and themes with real-time feedback.
-   **SEO Optimized**: Clean HTML structure and configurable metadata.

## 📋 Prerequisites

-   Python 3.10+
-   [Poetry](https://python-poetry.org/docs/#installation)

## 🛠️ Setup Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/5aharsh/papyro.git
    cd papyro
    ```

2.  **Install Dependencies**
    ```bash
    poetry install
    ```

3.  **Configure Environment**
    Copy the example environment file and adjust as needed:
    ```bash
    cp .env.example .env
    ```

4.  **Launch the Server**
    ```bash
    poetry run uvicorn papyro.main:app --reload
    ```
    Your site will be available at `http://127.0.0.1:8000`.

## ✍️ Content & Configuration

### Directory Override
By default, Papyro looks for content in `./papyro/content`. You can override this using an environment variable in your `.env` file:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `PAPYRO_CONTENT_DIR` | Path to your content folder (Markdown files and site-config.json). | `./papyro/content` |

### Site Settings
Manage global site metadata in `site-config.json` within your content directory.
```json
{
    "title": "My Papyro Blog",
    "theme": "papyro-default",
    "nav_order": ["about", "contact"]
}
```
*   **title**: The display name of your site.
*   **theme**: The folder name of your chosen theme (e.g., `papyro-typewriter`).
*   **nav_order**: An array of page slugs to control the order of links in the navigation bar.

### Blog Posts
Add `.md` files to the `posts/` subdirectory.
```markdown
---
title: My First Post
date: 2026-01-10
description: A short overview of this post.
slug: my-first-post
---
Content goes here...
```

### Static Pages
Add `.md` files to the `pages/` subdirectory. These automatically appear in your navigation bar.
```markdown
---
title: About Me
slug: about
---
Your bio goes here...
```

## 📁 Project Structure

```text
papyro/
├── content/           # Markdown files and site configuration
├── routers/           # Web routes and logic
├── services/          # Content indexing and rendering
├── static/            # CSS and assets (global)
├── templates/         # Jinja2 themes (default, typewriter)
├── utils/             # Config and template helpers
└── main.py            # Application entry point
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
