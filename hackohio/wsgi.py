import logging
from pyramid.config import Configurator

logger = logging.getLogger(__name__)

def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_static_view("/static", "hackohio:static/")

    logger.info("Creating WSGI server")
    config.scan()
    return config.make_wsgi_app()
