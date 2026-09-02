from typing import TypedDict, NotRequired
from pathlib import Path


class Config(TypedDict):
    pages: Path
    blogs: NotRequired[Path]
    dive_log: NotRequired[Path]
    base_url: NotRequired[str]
