# static-site-compiler

A Python-based static site compiler for generating a personal website from
Markdown files. Supports pages, blog posts and custom integrations (last.fm,
discogs, uddf dive logs).

Used to build [samiser.xyz](https://www.samiser.xyz).

Markdown content can be found here:
[site-content](https://github.com/Samiser/site-content)

> **Note**: This is a personal project, heavily customised for my specific needs
> and website structure. It's not designed for general use.

## How it works

Inspired by [john-doe.neocities.org](https://john-doe.neocities.org/), this
compiler generates a single `index.html` file containing the entire site. Each
page becomes a `<section>` element, and navigation uses anchor links (e.g.
`#blog`, `#about`) with CSS `:target` selectors to show/hide sections without
page reloads or JavaScript.

I think this is neat and fun, but I am cheating a little bit. Static content
like images, pdfs, and even style.css are separate and served from the `static/`
folder, which has many benefits for performance, caching, rendering etc. This
also means images can be lazy-loaded.

You could argue that having a bunch of separate html pages would also bring
benefits, but its not as fun!! And when the total size of the html is only about
100kB it's really not that big of a deal.

## Features

- **Markdown pages** with frontmatter support for title, navbar presence and
  page order (for navbar)
- **Blog posts** with automatic date grouping and syntax highlighting
- **Custom page integrations**:
  - Last.fm - display listening history
  - Discogs - display record collection
  - Dive log - display dive logs and notes

## Usage

```bash
# Access the package using your preferred method; here we use nix shell
nix shell github:samiser/static-site-compiler
ssc --pages <pages-dir> --out <output-dir> [options]
```

### Required arguments

- `--pages` - Directory containing Markdown page files
- `--out` - Output directory for the generated site

### Optional arguments

- `--blog-posts` - Directory containing blog post Markdown files
- `--dive-log` - Path to a UDDF dive log file
- `--secrets` - Path to secrets file (required for Last.fm/Discogs integrations)
- `--base-url` - Base URL of the deployed site, e.g. `https://example.com` (with `--blog-posts`, enables generating an RSS feed at `feed.xml`)

### Example

```bash
ssc --pages ./content/pages --blog-posts ./content/blog --out ./dist
```
