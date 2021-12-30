from pathlib import Path
from typing import Optional
from datetime import datetime

from loguru import logger
import typer
import os
import subprocess
import hashlib
from . import config

from .annex import Repo, FileKey

app = typer.Typer()

#repos = [ Repo(Path("~/PublicLibrary")), Repo(Path("~/PrivateLibrary")) ]

def detect_a_file(file: Path):
    key = FileKey(file)
    for r in config.repos:
        print(r.repo_path)
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
def clone(local_name : str, remote_name : str, repo_path : Path ):
    local_path = Path(repo_path.name).absolute()
    r = "origin"
    if remote_name:
        r = remote_name

    os.system(f"git clone -o {remote_name} {repo_path}")
    
    os.system(f"git -C {repo_path.name} annex init {local_name}")

    os.system(f"git -C {repo_path.name} annex sync")

    os.system(f"git -C {repo_path} remote add {local_name} {local_path}")


@app.command()
def init(local_name : str, local_path : Path ):
    os.system(f"mkdir {local_path}")
    os.system(f"git -C {local_path} init")
    os.system(f"git -C {local_path} annex init {local_name}")


@app.command()
def status():
    os.system(f"git status")

@app.command()
def sync():
    os.system(f"git annex sync")

@app.command()
def list():
    os.system(f"git annex list")

@app.command()
def add(path : Path, comment : Optional[str] = typer.Argument(None)):
    all_comment = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if comment:
        all_comment += ":" + comment
    os.system(f"git annex add {path}")
    os.system(f"git commit -m '{all_comment}'")

@app.command()
def help():
    typer.echo(f"Hello")

def cmd_ga():
    app()

