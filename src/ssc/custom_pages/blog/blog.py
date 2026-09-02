import re
import frontmatter
from collections import defaultdict
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import cast

from ssc.render import render_template
from ssc.parsers import parse_content, parse_files

from .types import Post, Posts, PostsByYear, Metadata
from ssc.secrets.types import Secrets
from ssc.config.types import Config
from ssc.parsers.types import Page


def _group_posts_by_year(posts: Posts) -> PostsByYear:
    titles_by_year: PostsByYear = defaultdict(list)

    for post in posts:
        post_date = cast(date, post["meta"]["date"])
        titles_by_year[str(post_date.year)].append(post)

    return titles_by_year


def parse_post(raw_md: frontmatter.Post):
    word_count = len(raw_md.content.strip().split(" "))
    time_to_read = round(word_count / 300)

    raw_tags = raw_md.metadata.get("tags")
    tags: list[str] = raw_tags if isinstance(raw_tags, list) else []
    title = str(raw_md.metadata["title"])
    summary = str(raw_md.metadata["summary"])
    date = raw_md.metadata["date"]
    publish = bool(raw_md.metadata["publish"])
    content = parse_content(raw_md.content)

    meta: Metadata = {
        "tags": tags,
        "title": title,
        "summary": summary,
        "date": date,
        "publish": publish,
        "time_to_read": time_to_read,
    }

    parsed: Post = {
        "content": content,
        "anchor": f"{date}-{title.lower().replace(' ', '-')}",
        "meta": meta,
    }

    return parsed


def parse_posts(dir: Path, exclude: list[str] | None = None) -> Posts:
    parsed = parse_files(dir, exclude, parse_post)
    return sorted(
        parsed,
        key=lambda x: str(x["meta"].get("date", "")),
        reverse=True,
    )


def create(_secrets: Secrets | None, config: Config) -> Page:
    blogs_dir = config.get("blogs")
    assert blogs_dir is not None
    posts = parse_posts(blogs_dir, exclude=["README.md"])

    html = render_template(
        Path(__file__).parent / "templates",
        "blog.html",
        {"blogs_by_year": _group_posts_by_year(posts)},
    )

    return Page(
        {"title": "blog", "content": html, "navbar": True, "type": "multi-page"}
    )


def _absolutize_urls(html: str, base_url: str) -> str:
    """Feed readers can't resolve relative or fragment urls in feed content."""
    html = re.sub(r'(src|href)="#', rf'\1="{base_url}/#', html)
    html = re.sub(r'(src|href)="/(?!/)', rf'\1="{base_url}/', html)
    html = re.sub(r'(src|href)="(?![a-z][a-z0-9+.-]*:|//)', rf'\1="{base_url}/', html)
    return html


def _rfc822_date(post_date: object) -> str:
    d = cast(date, post_date)
    return format_datetime(datetime(d.year, d.month, d.day, tzinfo=timezone.utc))


def create_feed(config: Config) -> str | None:
    blogs_dir = config.get("blogs")
    base_url = config.get("base_url")
    if blogs_dir is None or base_url is None:
        return None

    posts = parse_posts(blogs_dir, exclude=["README.md"])

    items = [
        {
            "title": post["meta"]["title"],
            "link": f"{base_url}/#{post['anchor']}",
            "pub_date": _rfc822_date(post["meta"]["date"]),
            # a literal "]]>" in post html would end the CDATA section early
            "content": _absolutize_urls(post["content"], base_url).replace(
                "]]>", "]]]]><![CDATA[>"
            ),
        }
        for post in posts
    ]

    return render_template(
        Path(__file__).parent / "templates",
        "feed.xml",
        {"base_url": base_url, "items": items},
    )
