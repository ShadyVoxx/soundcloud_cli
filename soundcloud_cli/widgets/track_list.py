from textual.containers import Vertical
from textual.message import Message
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import DataTable, Label, Input
from soundcloud_cli.api import SoundCloudClient
from soundcloud_cli.helper import truncate

class TrackList(Widget):
    
    class TrackSelected(Message):
        def __init__(self, track):
            self.track = track
            super().__init__()

    def __init__(self):
        super().__init__()
        self.client = SoundCloudClient()
        self.tracks = []

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Input(placeholder="Search tracks...", id="search-input")
            yield DataTable(id="track-table") 

    def on_mount(self) -> None:
        table = self.query_one("#track-table", DataTable)
        table.add_column("#", width=4)
        table.add_column("Title", width=40)
        table.add_column("Artist", width=15)
        table.add_column("Duration", width=8)
        table.cursor_type = "row"

    def on_data_table_row_selected(self, track_selected: DataTable.RowSelected):
        index = track_selected.row_key.value
        if index is None:
            return
        track_id = int(index)
        track = self.tracks[track_id]
        self.post_message(TrackList.TrackSelected(track))
        

    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if query:
            self.search(query)
    
    def search(self, query: str) -> None:
        self.tracks = self.client.search(query)
        table = self.query_one("#track-table", DataTable)
        table.clear()
        for i, track in enumerate(self.tracks):
            duration = track["duration"] // 1000
            mins = duration // 60
            secs = duration % 60
            track_title = truncate(track["title"], 40)
            track_artist = truncate(track["username"], 20)
            
            table.add_row(f"{i+1}",track_title,track_artist,f"{mins}:{secs:02d}",key=str(i))



    


