from textual.containers import Vertical, Center
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, Rule
from textual_image.widget import Image
from soundcloud_cli.helper import truncate, get_artwork_url
import requests
import os
import logging

logging.basicConfig(filename='/tmp/scc.log', level=logging.DEBUG)

CACHE_DIR = os.path.join(
    os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
    "soundcloud_cli"
)
os.makedirs(CACHE_DIR, exist_ok=True)

ARTWORK_PATH = os.path.join(CACHE_DIR, "artwork.jpg")

class TrackInfo(Widget):
    
    def compose(self) -> ComposeResult:
        with Vertical(id="track-info"):
            with Center(id="image-wrapper"):
                yield Image(id="image-placeholder")
            yield Rule(id="track-info-divider")
            with Vertical(id="track-info-text-grouping"):
                yield Label("Title: -", id="track-info-title-label")
                yield Label("Artist: -", id="track-info-artist-label")
                yield Label("Likes: -", id="track-info-plays-label")

    def update_label(self, track) -> None:

        self.app.log("update_label called")
        self.query_one("#track-info-title-label", Label).update(truncate(f"{track['title']}", length=28))
        self.query_one("#track-info-artist-label", Label).update(truncate(f"{track['username']}", length=28))
        self.query_one("#track-info-plays-label", Label).update(f"♥ {track['playback_count']:,}")

        artwork_url = get_artwork_url(track['artwork_url'])
        if artwork_url is None:
            return

        try:
            response = requests.get(artwork_url)
            with open(ARTWORK_PATH, "wb") as f:
                f.write(response.content)

            image_widget = self.query_one("#image-placeholder", Image)
            image_widget.image = ARTWORK_PATH
        except Exception as e:
            logging.error(f"Failed to display artwork: {e}")

