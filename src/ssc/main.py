#!/usr/bin/env python

from ssc.args import get_args
from ssc.site import build
from ssc.filesystem import write_file

from ssc.custom_pages import generate, blog


def main():
    args = get_args()

    custom_pages = generate(args["config"], args["secrets"])

    build(args["config"], custom_pages, args["out"])

    feed = blog.create_feed(args["config"])
    if feed is not None:
        write_file(args["out"] / "feed.xml", feed)


if __name__ == "__main__":
    main()
