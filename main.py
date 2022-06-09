import jinja2
import aiohttp_jinja2
from aiohttp import web
from app.routes import setup_routes
from app.models import pg_context
from configuration.settings import config, BASE_DIR

app = web.Application()

app['configuration'] = config


aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(str(BASE_DIR / 'templates')))

setup_routes(app)

app.cleanup_ctx.append(pg_context)

web.run_app(app)
