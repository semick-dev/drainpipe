from asyncio import subprocess
from typing import List
import os, sys, argparse
from subprocess import check_output

root_dir = os.path.dirname(__file__)


def locate_current_pip_folder() -> str:
    python_executable_folder = os.path.abspath(os.path.join(os.path.dirname(sys.executable), ".."))

    for root, _, _ in os.walk(python_executable_folder, topdown=True):
        # os.walk traverses top down. The very first directory that matches site-packages/pip
        # will be the target
        if os.path.join("site-packages", "pip") in root:
            return root


def get_current_pip_version() -> str:
    result = check_output([sys.executable, "-m", "pip", "--version"])
    return str(result).split(" ")[1]


def locate_target_file() -> str:
    return os.path.join(locate_current_pip_folder(), "_internal", "operations", "prepare.py")


def locate_backup_file() -> str:
    return os.path.join(os.path.dirname(locate_target_file()), "prepare_bkp.py")


def get_modification_index(lines: List[str]) -> int:
    for idx, line in enumerate(lines):
        if "REPLACE_ME" in line:
            return idx
    raise Exception('Unable to locate a "REPLACE_ME" line.')


def patch_function(line_array: List[str], target_dir: str) -> None:
    pip_version = get_current_pip_version()
    patch = os.path.join(root_dir, "compatibility_patches", pip_version, "unpack_url.py")

    if os.path.exists(patch):
        with open(patch, "r") as f:
            lines = f.readlines()
            index = get_modification_index(lines)
    else:
        raise Exception(
            'The current version of pip "{}" is not supported by drainpipe at this time.'.format(pip_version)
        )

    lines[index] = lines[index].replace("REPLACE_ME", target_dir.replace("\\", "/"))

    line_array.extend(lines)


def patch_pip_file(target_dir: str) -> None:
    prepare_py = locate_target_file()
    append = True
    lines = []

    with open(prepare_py, "r") as f:
        data = f.readlines()

    for line in data:
        if line.startswith("def unpack_url("):
            patch_function(lines, target_dir)
            append = False

        if append:
            lines.append(line)

        if line.startswith("    return file"):
            append = True

    # take backup!
    with open(locate_backup_file(), "w") as f:
        f.writelines(data)

    with open(prepare_py, "w") as f:
        f.writelines(lines)


def unpatch_pip_file() -> None:
    prepare_py = locate_target_file()
    patch_file = locate_backup_file()

    if not os.path.exists(patch_file):
        print("Backup file does not exist. Exiting.")
        exit(1)

    with open(patch_file, "r") as f:
        data = f.readlines()

    with open(prepare_py, "w") as f:
        f.writelines(data)

    os.remove(patch_file)


def check_patch_status() -> bool:
    return os.path.exists(locate_backup_file())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "drainpipe",
        description="This package is used to patch and unpatch your current pip directory. "
        + "Failure to provide an output folder will result in no-op.",
    )

    parser.add_argument("command", choices=["drain", "plug"])
    parser.add_argument(
        "--dest", help="The targeted directory. If not provided, will fall back to value in DRAINPIPE_DIRECTORY."
    )
    args = parser.parse_args()

    if not args.dest:
        args.dest = os.path.abspath(os.getenv("DRAINPIPE_DIRECTORY"))

    if not args.dest:
        print(
            "Drainpipe MUST have a target folder defined either by argument 'dest' or environment variable DRAINPIPE_DIRECTORY."
        )
        exit(1)

    if args.command == "drain":
        if not check_patch_status():
            patch_pip_file(args.dest)
            print('Draining pip downloads to "{}"'.format(args.dest))
        else:
            print("Already draining the pip pipe. No-op exiting.")
    else:
        if check_patch_status:
            unpatch_pip_file()
            print("Plugged draining downloads. Restored pip to regular operations.")
        else:
            print("Not currently in need of plugging the drain. No-op exiting.")
