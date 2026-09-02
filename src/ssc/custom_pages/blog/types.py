from typing import TypeAlias, TypedDict
from collections import defaultdict


class Metadata(TypedDict):
    tags: list[str]
    title: str
    summary: str
    date: object
    publish: bool
    time_to_read: int


class Post(TypedDict):
    content: str
    anchor: str
    meta: Metadata


Posts: TypeAlias = list[Post]
PostsByYear: TypeAlias = defaultdict[str, Posts]
