import logging
from pyramid.config import Configurator
from pyramid.view import view_config

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_static_view("/static", "hackohio:static/")

    # Config jinja2 renderer
    config.include("pyramid_jinja2")
    config.add_jinja2_renderer(".html")
    config.add_jinja2_search_path("hackohio:html/", ".html")

    # Routes
    config.add_route("index", "/")

    logger.info("Creating WSGI server")
    config.scan()
    return config.make_wsgi_app()


@view_config(route_name="index", renderer="index.html", request_method="GET")
def index_view(request):
    return {}
