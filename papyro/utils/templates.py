from fastapi.templating import Jinja2Templates
from papyro.utils.config import get_theme_path, load_config
from papyro.services import content_service
def get_templates():
    theme_dir = get_theme_path()
    templates = Jinja2Templates(directory=theme_dir)
    
    # Inject pages and config into all templates
    templates.env.globals["get_pages"] = content_service.get_pages
    templates.env.globals["config"] = load_config()
    
    return templates

templates = get_templates()
