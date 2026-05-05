# SoundCloud CLI

A terminal-based SoundCloud player I built because I wanted to listen to music without leaving my terminal. No Electron, no browser tabs — just search, pick a track, and hit play.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Why?

I spend most of my day in the terminal and I got tired of switching to a browser every time I wanted to play something on SoundCloud. I couldn't find a lightweight CLI tool that did what I wanted, so I made one. It hooks into SoundCloud's API, streams audio through mpv, and wraps everything in a nice TUI using [Textual](https://github.com/Textualize/textual).

## What it looks like

The interface is split into two panels:

- **Left** — a search bar and results table showing track title, artist, and duration
- **Right** — album art, track name, artist, and play count for whatever track you've selected

There's a now-playing bar pinned at the bottom with a seekable progress bar, timestamps, and volume info. The whole thing uses SoundCloud's orange (`#ff5500`) as an accent color so it actually feels on-brand.

## Features

- **Search** — type a query, hit enter, get results
- **Stream** — plays audio through mpv (no video, obviously)
- **Album art** — pulls high-res artwork and renders it right in the terminal using `textual-image`
- **Seekable progress bar** — click anywhere on the bar to jump to that position
- **Track info panel** — shows the selected track's metadata at a glance
- **Config file** — stores your `client_id` in `~/.config/soundcloud_cli/config.json` with `0600` permissions so it's not sitting around world-readable

## Dependencies

You'll need these installed before running:

- **Python 3.10+**
- **mpv** — handles the actual audio playback
- **Textual** — the TUI framework
- **textual-image** — for rendering album art in the terminal
- **requests** — for API calls

Install the Python deps:

```bash
pip install textual textual-image requests
```

And make sure mpv is installed on your system:

```bash
# Debian / Ubuntu / Kali
sudo apt install mpv

# Arch
sudo pacman -S mpv

# macOS
brew install mpv
```

## Setup

1. Clone the repo:

```bash
git clone https://github.com/ShadyVoxx/soundcloud_cli.git
cd soundcloud_cli
```

2. Add your SoundCloud `client_id` to the config file:

```bash
mkdir -p ~/.config/soundcloud_cli
echo '{"client_id": "YOUR_CLIENT_ID_HERE"}' > ~/.config/soundcloud_cli/config.json
chmod 600 ~/.config/soundcloud_cli/config.json
```

If you don't know how to get a client ID — open SoundCloud in your browser, open DevTools, go to the Network tab, and look for `client_id` in the query parameters of any API request. It's not hidden.

3. Run it:

```bash
python -m soundcloud_cli.ui
```

## Project structure

```
soundcloud_cli/
├── main.py                  # Quick test entrypoint
├── app.tcss                 # Textual stylesheet (theming & layout)
└── soundcloud_cli/
    ├── __init__.py
    ├── api.py               # SoundCloud API client
    ├── config.py            # Config file management
    ├── helper.py            # Utility functions (truncation, artwork URLs)
    ├── player.py            # mpv wrapper using IPC socket
    ├── ui.py                # Main Textual app
    └── widgets/
        ├── __init__.py
        ├── now_playing_bar.py   # Bottom bar with progress + seek
        ├── search_bar.py
        ├── track_info.py        # Right panel (artwork + metadata)
        └── track_list.py        # Left panel (search + results table)
```

## How it works (briefly)

- `api.py` talks to `api-v2.soundcloud.com` to search tracks and resolve progressive stream URLs
- `player.py` spawns an mpv subprocess with `--no-video` and communicates through a Unix domain socket (`mpv --input-ipc-server`) for play/pause/seek/volume
- `ui.py` ties it all together in a Textual app — polls playback position every second, updates the progress bar, and dispatches messages between widgets
- Album art gets downloaded to `~/.cache/soundcloud_cli/artwork.jpg` and rendered via `textual-image`

## A note on AI usage

I wrote all the core logic myself — the API client, mpv IPC integration, widget architecture, and application flow. AI was used to help with the **styling and theming** (the `.tcss` stylesheet, color choices, layout tweaks) to make the interface look polished. The actual functionality and code structure is all me.

## Known limitations

- Only plays tracks that have a progressive stream available (most do, some don't)
- No playlist support yet — it's single-track playback for now
- The `client_id` can stop working if SoundCloud rotates it — you'll need to grab a fresh one
- No offline caching of tracks

## License

MIT — do whatever you want with it.

---

*Built because tab-switching to a browser for music is a mass productivity killer.*
