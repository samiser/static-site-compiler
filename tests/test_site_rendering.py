import pytest
from pytest import TempPathFactory
from expecttest import assert_expected_inline
from pathlib import Path
from xml.etree import ElementTree

from ssc.site import build
from ssc.filesystem import write_file
from ssc.secrets.types import Secrets
from ssc.config.types import Config
from ssc.custom_pages import blog


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("site")


@pytest.fixture(scope="module")
def built_site(site_dir: Path) -> Path:
    """Builds the site once and returns the output directory."""
    test_data_path = Path(__file__).parent / "test_data"

    secrets: Secrets = {
        "lastfm": {"api_key": "boop", "shared_secret": "boop"},
        "discogs": {"token": "boop"},
        "letterboxd": {"username": "boop", "password": "boop"},
    }

    config: Config = {
        "blogs": test_data_path / "blogs",
        "pages": test_data_path / "pages",
        "base_url": "https://example.com",
    }

    build(config, [blog.create(secrets, config)], site_dir)

    feed = blog.create_feed(config)
    assert feed is not None
    write_file(site_dir / "feed.xml", feed)

    return site_dir


def directory_tree(path: Path, level: int = 0) -> str:
    tree_str = f"{'  ' * level}- {path.name}\n"
    if path.is_dir():
        for child in sorted(path.iterdir()):
            tree_str += directory_tree(child, level + 1)
    return tree_str


def test_site_structure(built_site: Path):
    assert_expected_inline(
        directory_tree(built_site),
        """\
- site0
  - boop
    - blog_static_file
    - page_static_file
  - favicon.ico
  - feed.xml
  - images
    - blog_image
    - page_image
    - twitter.jpg
  - index.html
  - style.css
""",
    )


def test_main_rendering(built_site: Path):
    rendered_index = (built_site / "index.html").read_text()
    assert_expected_inline(
        rendered_index,
        """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />

    <title>Samiser</title>
    <meta name="description" content="Samiser's space on the internet" />

    <!-- twitter card -->
    <meta property="og:title" content="Samiser" />
    <meta property="og:description" content="my space on the internet" />
    <meta
      property="og:image"
      content="https://images.samiser.xyz/location.png"
    />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="stylesheet" href="style.css" />
    <link rel="alternate" type="application/rss+xml" title="Samiser's blog" href="feed.xml" />
    </head>
  <body>
    <header>
  <h1>
    <a href="#home">Samiser</a>
  </h1>
  <nav>
    <a href="#test">Test</a>
    <a href="#blog">blog</a>
  </nav>
</header> <main><section id="test">
    <h1>Test</h1>
    <hr />
<p>test page</p>
<p>with a <a href="#blog">link!</a></p>
  </section><section id="blog">
  <h1>blog</h1>
  <hr>
  <p>occasionally i like writing about things here</p>
  <h2>2000</h2>
  <ul>
    <li><a href="#2000-01-01-test-page"><em>2000-01-01</em> - Test page</a></li>
  </ul>
</section>
<section id="2000-01-01-test-page">
  <h1>Test page</h1>
  <p><em>2000-01-01</em></p>
  <p><em>0 minute read</em></p>
  <hr>
  <p>This is a test!</p>
<p><img loading="lazy" alt="an image" src="images/blog_image.png" /></p>
<p>A <a href="#blog">fragment link</a> and an <a href="https://example.org">absolute link</a>.</p>
<div class="codehilite"><pre><span></span><code><span class="k">def</span><span class="w"> </span><span class="nf">hello</span><span class="p">():</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;test&quot;</span><span class="p">)</span>
</code></pre></div>
  <hr>
  <a href="#blog">Back</a>
</section>
</main>
  </body>
</html>""",
    )


def test_feed_is_valid_xml(built_site: Path):
    root = ElementTree.fromstring((built_site / "feed.xml").read_text())
    assert len(root.findall(".//item")) == 1


def test_feed_requires_url():
    test_data_path = Path(__file__).parent / "test_data"
    config: Config = {
        "blogs": test_data_path / "blogs",
        "pages": test_data_path / "pages",
    }
    assert blog.create_feed(config) is None


def test_feed_rendering(built_site: Path):
    rendered_feed = (built_site / "feed.xml").read_text()
    assert_expected_inline(
        rendered_feed,
        """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Samiser's blog</title>
    <link>https://example.com/#blog</link>
    <atom:link href="https://example.com/feed.xml" rel="self" type="application/rss+xml"/>
    <description>occasionally i like writing about things here</description>
    <item>
      <title>Test page</title>
      <link>https://example.com/#2000-01-01-test-page</link>
      <guid isPermaLink="true">https://example.com/#2000-01-01-test-page</guid>
      <pubDate>Sat, 01 Jan 2000 00:00:00 +0000</pubDate>
      <description><![CDATA[<p>This is a test!</p>
<p><img loading="lazy" alt="an image" src="https://example.com/images/blog_image.png" /></p>
<p>A <a href="https://example.com/#blog">fragment link</a> and an <a href="https://example.org">absolute link</a>.</p>
<div class="codehilite"><pre><span></span><code><span class="k">def</span><span class="w"> </span><span class="nf">hello</span><span class="p">():</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;test&quot;</span><span class="p">)</span>
</code></pre></div>]]></description>
    </item>
    </channel>
</rss>""",
    )
