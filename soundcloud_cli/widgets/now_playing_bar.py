from typing import cast
from textual.containers import Horizontal
from textual.getters import query_one
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, ProgressBar
from textual.events import Click

class NowPlayingBar(Widget):
    title = reactive("Nothing Playing")
    artist = reactive("")
    duration = reactive(0.0)
    position = reactive(0.0)
    volume = reactive(0.0)

    class Seeked(Message):
        def __init__(self, position:float) -> None:
            self.position = position
            super().__init__()

    class SeekableProgressBar(ProgressBar):
        DEFAULT_CSS = """
    SeekableProgressBar Bar {
        color: #ff5500;
        background: #333333;
    }
    """
        def on_click(self, event: Click) -> None:
            if self.size.width == 0:
                return
            percentage = event.x / self.size.width
            seek_pos = self.app.query_one(NowPlayingBar).duration * percentage
            self.post_message(NowPlayingBar.Seeked(seek_pos))



    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("", id="now-playing-label-left")
            yield self.SeekableProgressBar(id="progress-bar", show_eta=False, show_percentage=False)
            yield Label("", id="now-playing-label-right")
    
    #WATHCER FUNCTIONS
    def watch_duration(self, value: float) -> None:
        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(total=value)

    def watch_title(self, value: str) -> None:
        text = f"{self.title} - {self.artist}"
        left_label = self.query_one("#now-playing-label-left", Label)
        left_label.update(text)
        self._update_label()

    def watch_position(self, value: float) -> None:
        self._update_label()

    def watch_artist(self, value: str) -> None:
        self._update_label()

    #UPDATE
    def _update_label(self):
        pos_mins = int(self.position) // 60
        pos_secs = int(self.position) % 60
        dur_mins = int(self.duration) // 60
        dur_secs = int(self.duration) % 60

        bar = self.query_one("#progress-bar", self.SeekableProgressBar)
        bar.progress = self.position
        right_label = self.query_one("#now-playing-label-right", Label)
        text = f"{pos_mins}:{pos_secs:02d} / {dur_mins}:{dur_secs:02d} Vol:{self.volume}"
        right_label.update(text)
