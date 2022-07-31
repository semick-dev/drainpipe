from typing import List
import pdb, os, sys, argparse


def locate_current_pip_folder() -> str:
    return os.path.join(os.path.dirname(sys.executable), "..", "Lib", "site-packages", "pip")


def locate_target_file() -> str:
    return os.path.join(locate_current_pip_folder(), "_internal", "operations", "prepare.py")


def locate_backup_file() -> str:
    return os.path.join(os.path.dirname(locate_target_file()), "prepare_bkp.py")


def patch_function(line_array: List[str], target_dir: str) -> None:
    with open("./unpack_url.py", "r") as f:
        lines = f.readlines()

    lines[58] = lines[58].replace("REPLACE_ME", target_dir)

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
        "Failure to provide an output folder will result in no-op.",
    )

    parser.add_argument("command", choices=["drain", "plug"])
    parser.add_argument("--dest", help="The targeted directory. If not provided, will fall back to value in")
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
