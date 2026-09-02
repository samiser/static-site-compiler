import os
import shutil
from pathlib import Path


def _copy_with_write_permissions(src: str, dst: str):
    _ = shutil.copy(src, dst)
    os.chmod(dst, 0o644)


def copy_files(source_dir: Path, dest_dir: Path):
    _ = shutil.copytree(
        source_dir,
        dest_dir,
        dirs_exist_ok=True,
        copy_function=_copy_with_write_permissions,
    )
    for path in dest_dir.rglob("*"):
        if path.is_dir():
            path.chmod(0o755)
    dest_dir.chmod(0o755)
    print(f"Copied files from {source_dir} to {dest_dir}")


def write_index_html(out_path: Path, output: str):
    outfile = out_path / "index.html"

    with outfile.open(mode="w") as f:
        _: int = f.write(output)
        print(f"Blog compiled and written to {outfile}")


def write_file(outfile: Path, output: str):
    with outfile.open(mode="w") as f:
        _: int = f.write(output)
        print(f"Written to {outfile}")
