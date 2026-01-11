import os
import frontmatter
import markdown
from typing import List, Dict, Optional
from papyro.utils.config import get_content_dir, load_config, KEY_NAV_ORDER

CONTENT_DIR = get_content_dir()

def get_posts() -> List[Dict]:
    """Get all blog posts, sorted by date descending."""
    posts = []
    posts_dir = CONTENT_DIR / "posts"
    
    if not posts_dir.exists():
        return []

    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            file_path = posts_dir / filename
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                posts.append({
                    "slug": post.metadata.get("slug", filename.replace(".md", "")),
                    "title": post.metadata.get("title", "Untitled"),
                    "date": post.metadata.get("date"),
                    "description": post.metadata.get("description", ""),
                    "content": post.content
                })
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    return posts

def get_post(slug: str) -> Optional[Dict]:
    """
    Get a single post by slug.
    Note: In a real app with many files, we'd map slugs to filenames efficiently.
    For now, we'll just scan or assume filename matches slug if standard conventions used,
    but scanning is safer if slug != filename.
    """
    posts = get_posts()
    for post in posts:
        if post["slug"] == slug:
            # Convert markdown to HTML here just for the single view
            post["html_content"] = markdown.markdown(
                post["content"],
                extensions=['extra', 'pymdownx.tilde', 'codehilite']
            )
            return post
    return None

def get_page(slug: str) -> Optional[Dict]:
    """
    Get a static page by slug (e.g. 'about').
    """
    pages_dir = CONTENT_DIR / "pages"
    # Try finding file directly or scanning
    # Simple approach: scan like posts
    if not pages_dir.exists():
        return None
        
    for filename in os.listdir(pages_dir):
        if filename.endswith(".md"):
            file_path = pages_dir / filename
            with open(file_path, "r", encoding="utf-8") as f:
                page = frontmatter.load(f)
                current_slug = page.metadata.get("slug", filename.replace(".md", ""))
                if current_slug == slug:
                    return {
                        "slug": current_slug,
                        "title": page.metadata.get("title", "Untitled"),
                        "html_content": markdown.markdown(
                            page.content,
                            extensions=['extra', 'pymdownx.tilde', 'codehilite']
                        )
                    }
    return None


def get_pages() -> List[Dict]:
    """Get all static pages, sorted by config.nav_order."""
    pages = []
    pages_dir = CONTENT_DIR / "pages"
    
    if not pages_dir.exists():
        return []

    for filename in os.listdir(pages_dir):
        if filename.endswith(".md"):
            file_path = pages_dir / filename
            with open(file_path, "r", encoding="utf-8") as f:
                page = frontmatter.load(f)
                pages.append({
                    "slug": page.metadata.get("slug", filename.replace(".md", "")),
                    "title": page.metadata.get("title", "Untitled"),
                })
    
    # Load config and sort
    config = load_config()
    nav_order = config.get(KEY_NAV_ORDER, [])
    
    # Map slug to index for easy sorting
    # Default to a large number so unlisted pages go to the end
    order_map = {slug: i for i, slug in enumerate(nav_order)}
    
    def sort_key(page):
        slug = page["slug"]
        # If in config, return its index. If not, return large number + alphabetical tie-breaker
        if slug in order_map:
            return (0, order_map[slug])
        return (1, slug)
        
    pages.sort(key=sort_key)
    return pages
