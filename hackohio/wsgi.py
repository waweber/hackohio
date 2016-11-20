import logging
from pyramid.config import Configurator
from pyramid.view import view_config
from hackohio.mood import Mood
from hackohio.secrets import get_secret
from hackohio import soundcloud

logger = logging.getLogger(__name__)

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_debugtoolbar")

    config.add_static_view("/static", "hackohio:static/")

    # Config jinja2 renderer
    config.include("pyramid_jinja2")
    config.add_jinja2_renderer(".html")
    config.add_jinja2_search_path("hackohio:html/", ".html")

    # Routes
    config.add_route("index", "/")
    config.add_route("playlist", "/playlist/{name}")
    config.add_route("soundcloud_tracks", "/soundcloud/tracks")
    config.add_route("soundcloud_streams", "/soundcloud/streams")

    for mood_provider in ["webcam", "voice", "twitter"]:
        config.add_route("mood#%s" % mood_provider, "/mood/%s" % mood_provider)

    logger.info("Creating WSGI server")
    config.scan()
    return config.make_wsgi_app()


@view_config(route_name="index", renderer="index.html", request_method="GET")
def index_view(request):
    client_id = get_secret("soundcloud", "client_id")
    return {"client_id": client_id}

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
            "media": "/static/media/sad1.mp3",
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
    if name == "angry":
        return [{
            "media": "/static/media/angry1.mp3",
            "cover": "/static/media/angry1.jpg",
            "title": "Angry Song 1",
            "artist": "Angry Guy",
            "album": "Angry Album",
        }, {
            "media": "/static/media/angry2.ogg",
            "cover": "/static/media/angry2.jpg",
            "title": "Angry Song 2",
            "artist": "Angry Guy",
            "album": "Angry Album 2",
        }, {
            "media": "/static/media/angry3.ogg",
            "cover": "/static/media/angry3.jpg",
            "title": "Angry Song 3",
            "artist": "Angry Person",
            "album": "Angry II",
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

@view_config(route_name="mood#twitter", renderer="json", request_method="GET")
def mood_twitter_view(request):
    twitter_handle = request.GET.get('handle')

    return {
        "mood": Mood.mood_from_twitter(twitter_handle)
    }

@view_config(route_name="mood#webcam", renderer="string", request_method="POST")
def mood_webcam_view(request):
    picture = request.POST.get('webcam').file

    # TODO: Check validity? Resize?

    try:
        mood = Mood.mood_from_picture(picture)
        logger.debug("Mood: %r" % mood)
        return mood
    except Exception as e:
        logger.debug("microsoft picture api failed", exc_info=True)
        return "none"

@view_config(route_name="soundcloud_tracks", renderer="json",
        request_method="GET")
def soundcloud_tracks(request):
    playlist_id = request.GET.get("playlist_id")

    return soundcloud.get_playlist_tracks(playlist_id)

@view_config(route_name="soundcloud_streams", renderer="json",
        request_method="GET")
def soundcloud_streams(request):
    track_id = request.GET.get("track_id")

    return soundcloud.get_stream_url(track_id)
