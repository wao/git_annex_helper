from pathlib import Path
from typing import Optional

from loguru import logger
import typer
import os
import subprocess
import hashlib

app = typer.Typer()

def genkey_sha256e(file : Path):
    sha256 = subprocess.check_output(["/usr/bin/sha256sum",file]).decode("utf-8").split(" ")[0]
    size=file.stat().st_size
    ext=file.suffix
    return f"SHA256E-s{size}--{sha256}{ext}"

OLD_ENCODE_STR="0123456789zqjxkmvwgpfZQJXKMVWGPF"

def gendir_old(key: str):
    md5_bytes = hashlib.md5(key.encode("utf-8")).digest()
    b0 = OLD_ENCODE_STR[md5_bytes[0] % 32]
    b1 = OLD_ENCODE_STR[md5_bytes[0] // 64 + (md5_bytes[1]%8)*4]
    b2 = OLD_ENCODE_STR[md5_bytes[1] // 16 + md5_bytes[2] % 2 * 16 ]
    b3 = OLD_ENCODE_STR[md5_bytes[2] // 4 % 32 ]

    return f"{b1}{b0}/{b3}{b2}"

class FileKey:
    def __init__(this, file : Path):
        this.path = file
        this.sha256e_key = genkey_sha256e(file)
        this.old_dir = gendir_old(this.sha256e_key)

class Repo:
    def __init__(this, repo_path : Path):
        this.repo_path = repo_path.expanduser()

    def detect(this, file : FileKey ):
        link_dir_path = Path( this.repo_path, ".git/annex/objects", file.old_dir, file.sha256e_key )
        return link_dir_path.exists()

repos = [ Repo(Path("~/PublicLibrary")), Repo(Path("~/PrivateLibrary")) ]

def detect_a_file(file: Path):
    key = FileKey(file)
    for r in repos:
        if r.detect(key):
            typer.echo(f"Y {file} -in- {r.repo_path}")
            break
    else:
        typer.echo(f"N {file}")


def detect_all_files_under_dir(path : Path):
    for fn in path.rglob("*.*"):
        if fn.is_file():
            detect_a_file(fn)

@app.command()
def detect(file: Path):
    #typer.echo(f"Detect existends for {file}")

    if file.is_file():
        detect_a_file(file)
    elif file.is_dir():
        detect_all_files_under_dir(file)

@app.command()
def help():
    typer.echo(f"Hello")

def cmd_ga():
    app()
