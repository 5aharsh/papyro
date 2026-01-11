from fastapi import APIRouter, Request, HTTPException
from papyro.services import content_service
from papyro.utils.templates import templates

router = APIRouter()


@router.get("/post/{slug}")
async def get_post(slug: str, request: Request):
    post = content_service.get_post(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post.html", {"request": request, "post": post})

@router.get("/page/{slug}")
async def get_page(slug: str, request: Request):
    page = content_service.get_page(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse("page.html", {"request": request, "page": page})
