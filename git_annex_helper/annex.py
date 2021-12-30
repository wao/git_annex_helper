import subprocess
import hashlib
from pathlib import Path

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
