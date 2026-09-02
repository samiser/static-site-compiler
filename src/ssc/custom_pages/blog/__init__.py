__all__: list[str] = []


# only import create/create_feed if that's what is being imported
def __getattr__(name: str):
    if name in ("create", "create_feed"):
        from . import blog

        attr = getattr(blog, name)
        globals()[name] = attr
        __all__.append(name)
        return attr
    raise AttributeError(f"module {__name__} has no attribute {name}")
