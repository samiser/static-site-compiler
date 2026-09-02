from setuptools import setup

_ = setup(
    name="static-site-compiler",
    version="0.1.0",
    description="my cool static site compiler",
    author="Samiser",
    entry_points={
        "console_scripts": [
            "ssc = ssc.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ssc": [
            "custom_pages/*/templates/*.html",
            "custom_pages/*/templates/*.xml",
            "site/templates/*.html",
            "static/*",
            "static/*/*",
        ],
    },
    install_requires=[
        "Jinja2",
        "Markdown",
        "Pygments",
        "python-frontmatter",
        "requests",
    ],
)
