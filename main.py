import sys
import tempfile
import argparse
import toml
import os

from git import Repo


def run(repo_url: str, verbose: bool):
    print(f"Installing {repo_url} ...")

    PREFIX = {
        "win32": os.environ.get("AppData", ""),
        "linux": os.environ.get("XDG_DATA_HOME", ""),
        "darwin": "~/Library/Caches",
    }[sys.platform]

    with tempfile.TemporaryDirectory() as temp_dir:
        Repo.clone_from(repo_url, temp_dir)
        try:
            config = toml.load(temp_dir + "/typst.toml")
            name = config["package"]["name"]
            version = config["package"]["version"]
        except Exception as e:
            if verbose:
                print(e)
            print("Aborting, missing or invalid typst.toml file")
            return

        package_root = os.path.normpath(f"{PREFIX}/typst/packages/local/{name}")
        this_package = os.path.normpath(f"{package_root}/{version}")

        try:
            os.makedirs(package_root)
            os.rename(temp_dir, this_package)
        except FileExistsError:
            print(f"Aborting: {name}:{version} already installed at {this_package}")
            return

    print(f'Successfully installed, import with:\n\n#import "@local/{name}:{version}"')


def main():
    parser = argparse.ArgumentParser(
        "typkg", description="(git) package installer for typst"
    )
    parser.add_argument("repository_url")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    run(args.repository_url, args.verbose)
