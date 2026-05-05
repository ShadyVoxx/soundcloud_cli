from sys import exception
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import TabbedContent, TabPane


from soundcloud_cli.widgets import NowPlayingBar
from soundcloud_cli.widgets.track_list import TrackList
from soundcloud_cli.widgets.track_info import TrackInfo
from soundcloud_cli.api import SoundCloudClient
from soundcloud_cli.player import Player

class SoundCloudApp(App):
    CSS_PATH = "../app.tcss"
    TITLE = "SoundCloud CLI"
    SUB_TITLE = "Nothing Playing"

    
    def __init__(self):
        super().__init__()
        self.client = SoundCloudClient()
        self.player = Player()
    
 
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Search"):
                with Horizontal():
                    yield TrackList()
                    yield TrackInfo()
        yield NowPlayingBar()

    def on_mount(self) -> None:
        self.set_interval(1, self.update_progress)

    def update_progress(self) -> None:
        if self.player.is_playing():
            try:
                bar = self.query_one(NowPlayingBar)
                bar.position = self.player.get_position()
            except Exception:
                pass
        else:
            bar = self.query_one(NowPlayingBar)
            if bar.position > 0:
                bar.position = 0.0
                bar.artist = ""
                bar.duration = 0.0
                self.sub_title = "Nothing Playing"
                
                bar.title = "Nothing Playing"
    def on_track_list_track_selected(self, message: TrackList.TrackSelected):
        try:
            url = self.client.get_stream_url(message.track["transcodings"])
            self.player.play(url)
            #BAR UPDATE
            bar = self.query_one(NowPlayingBar)
            bar.artist = message.track["username"]
            bar.title = message.track["title"]
            bar.duration = message.track["duration"] / 1000
            self.sub_title = f"{message.track['title']} — {message.track['username']}"

            #TRACKINFO UPDATE
            track_info = self.query_one(TrackInfo)
            track_info.update_label(message.track)
    
        except ValueError as e:
            self.notify(str(e), severity="error")

    def on_now_playing_bar_seeked(self, message: NowPlayingBar.Seeked):
        try:
            seek_position = message.position
            self.player.seek(seek_position)
            bar = self.query_one(NowPlayingBar)
            bar.position = message.position
        except ValueError as e:
            self.notify(str(e), severity="error")


    def on_unmount(self) -> None:
        self.player.stop()

if __name__== "__main__":
    app = SoundCloudApp()
    app.run()
