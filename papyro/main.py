from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from papyro.routers import blog
from papyro.services import content_service

from papyro.utils.config import get_theme_path, load_config, KEY_TITLE, validate_content_dir, ContentDirectoryError
from papyro.utils.templates import templates

# Early validation for app configuration
try:
    validate_content_dir()
    config = load_config()
except ContentDirectoryError:
    config = {KEY_TITLE: "Papyro - Configuration Error", KEY_THEME: "papyro-default"}

app = FastAPI(title=config[KEY_TITLE])

# Exception handler for ContentDirectoryError (500)
@app.exception_handler(ContentDirectoryError)
async def content_dir_exception_handler(request: Request, exc: ContentDirectoryError):
    return templates.TemplateResponse(
        "error.html", 
        {
            "request": request,
            "error_title": "Configuration Error",
            "error_message": exc.message,
            "config": config
        }, 
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# Exception handler for 404 Not Found
@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_title": "404 - Not Found",
            "error_message": exc.detail if hasattr(exc, 'detail') else "The page you are looking for doesn't exist.",
            "config": config
        },
        status_code=status.HTTP_404_NOT_FOUND
    )

# Middleware to enforce content directory availability
@app.middleware("http")
async def check_content_dir_middleware(request: Request, call_next):
    if not request.url.path.startswith("/static"):
        try:
            validate_content_dir()
        except ContentDirectoryError as exc:
            return await content_dir_exception_handler(request, exc)
    return await call_next(request)

# Mount static files to the active theme directory
theme_dir = get_theme_path()
app.mount("/static", StaticFiles(directory=theme_dir), name="static")

app.include_router(blog.router)

@app.get("/")
async def root(request: Request):
    posts = content_service.get_posts()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})
