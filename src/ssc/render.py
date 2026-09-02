import jinja2

from pathlib import Path
from ssc.custom_pages.lastfm.types import MyTopAlbums as LastFMTopAlbums
from ssc.custom_pages.discogs.types import Releases as DiscogsReleases
from ssc.custom_pages.dive_log.types import Dive
from ssc.custom_pages.blog.types import PostsByYear
from ssc.site.types import Pages


def render_template(
    template_dir: Path,
    template_file: str,
    template_vars: (
        LastFMTopAlbums
        | DiscogsReleases
        | dict[str, Pages | PostsByYear]
        | dict[str, Pages | bool]
        | dict[str, dict[int, Dive]]
        | dict[str, str | list[dict[str, str]]]
    ),
) -> str:
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template(template_file)

    rendered = template.render(template_vars)

    return rendered
