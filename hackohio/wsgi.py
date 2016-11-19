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
    config.add_route("playlist", "/playlist/{name}")

    logger.info("Creating WSGI server")
    config.scan()
    return config.make_wsgi_app()


@view_config(route_name="index", renderer="index.html", request_method="GET")
def index_view(request):
    return {}


@view_config(route_name="playlist", renderer="json", request_method="GET")
def playlist_view(request):
    name = request.matchdict.get("name")

    if name == "happy":
        return [{
            "media": "/static/media/happy1.ogg",
            "cover": "/static/media/happy1.jpg",
            "title": "Happy Song 1",
            "artist": "Happy Guy",
            "album": "Happy Album",
        }, {
            "media": "/static/media/happy2.ogg",
            "cover": "/static/media/happy2.jpg",
            "title": "Happy Song 2",
            "artist": "Happy Guy",
            "album": "Happy Album 2",
        }, {
            "media": "/static/media/happy3.ogg",
            "cover": "/static/media/happy3.jpg",
            "title": "Happy Song 3",
            "artist": "Happy Person",
            "album": "Happy II",
        }]
    elif name == "sad":
        return [{
            "media": "/static/media/sad1.ogg",
            "cover": "/static/media/sad1.jpg",
            "title": "Sad Song 1",
            "artist": "Sad Guy",
            "album": "Sad Album",
        }, {
            "media": "/static/media/sad2.ogg",
            "cover": "/static/media/sad2.jpg",
            "title": "Sad Song 2",
            "artist": "Sad Guy",
            "album": "Sad Album 2",
        }, {
            "media": "/static/media/sad3.ogg",
            "cover": "/static/media/sad3.jpg",
            "title": "Sad Song 3",
            "artist": "Sad Person",
            "album": "Sad II",
        }]
    else:
        return [{
            "media": "/static/media/normal1.ogg",
            "cover": "/static/media/normal1.jpg",
            "title": "Normal Song 1",
            "artist": "Normal Guy",
            "album": "Normal Album",
        }, {
            "media": "/static/media/normal2.ogg",
            "cover": "/static/media/normal2.jpg",
            "title": "Normal Song 2",
            "artist": "Normal Guy",
            "album": "Normal Album 2",
        }, {
            "media": "/static/media/normal3.ogg",
            "cover": "/static/media/normal3.jpg",
            "title": "Normal Song 3",
            "artist": "Normal Person",
            "album": "Normal II",
        }]
