import argparse
from typing import TypedDict, cast
from pathlib import Path

from ssc.secrets.types import Secrets
from ssc.secrets import load_secrets
from ssc.config.types import Config
from ssc.config import create_config


class Args(TypedDict):
    config: Config
    secrets: Secrets | None
    out: Path


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(description="sam's cool static site compiler")
    _ = parser.add_argument("--pages", required=True, help="pages directory")
    _ = parser.add_argument("--blog-posts", help="blog post directory")
    _ = parser.add_argument("--dive-log", help="dive log in uddf format")
    _ = parser.add_argument(
        "--base-url",
        help="base url of the deployed site (e.g. https://example.com), enables the rss feed",
    )
    _ = parser.add_argument("--secrets", help="secrets file path")
    _ = parser.add_argument("--out", required=True, help="output directory")
    args: argparse.Namespace = parser.parse_args()

    config = create_config(
        pages=Path(cast(str, args.pages)),
        blogs=Path(args.blog_posts) if args.blog_posts else None,
        dive_log=Path(args.dive_log) if args.dive_log else None,
        base_url=cast(str, args.base_url) if args.base_url else None,
    )

    secrets = load_secrets(Path(args.secrets)) if args.secrets else None

    return Args(
        config=config,
        secrets=secrets,
        out=Path(cast(str, args.out)),
    )


_args = None


def get_args() -> Args:
    global _args
    if _args is None:
        _args = _parse_args()
    return _args
