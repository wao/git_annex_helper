import json
import typer
from pathlib import Path
from flexdict import FlexDict
from .annex import Repo


def load_config(file_path: Path):
    return FlexDict(json.loads(file_path.read_text()))

def load_default_config():
    app_dir = typer.get_app_dir("git_annex_helper")
    config_path = Path(app_dir) / "config.json"
    print(config_path)
    if config_path.is_file():
        return load_config(config_path)

    return Dict()


cfg = load_default_config()

repos = [ Repo(Path(r)) for r in  cfg.get("repos", default=[]) ]

