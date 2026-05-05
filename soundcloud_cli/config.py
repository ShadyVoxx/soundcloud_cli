import json
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "soundcloud_cli" / "config.json"

def create_config_file():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({}, indent = 4))
    os.chmod(CONFIG_PATH, 0o600)


def load_config():
    if not CONFIG_PATH.exists():
        create_config_file()

    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_config_value(key, default=None):
    config_dict = load_config()
    return config_dict.get(key, default) 

def set_config_value(key, value):
    config_dict = load_config()
    config_dict[key] = value

    with open(CONFIG_PATH, "w") as f:
        json.dump(config_dict, f, indent=4)










