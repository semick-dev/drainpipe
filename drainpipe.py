from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import List

def locate_current_pip_folder() -> str:
    pass

def locate_target_file(pip_install_folder: str) -> str:
    # _internal/operations/prepare.py
    pass

def patch_function(line_array: List[str]) -> None:
    with open('./unpack_url.py', 'r') as f:
        lines = f.readlines()

    line_array.extend(lines)

def patch_target_file(prepare_py: str) -> None:
    with open(prepare_py, 'r') as f:
        data = f.readlines()

    append = True
    lines = []

    for line, content in enumerate(data):
        if line.startswith("def unpack_url("):
            append = False
        
        if append:
            lines.append(line)

        if line.startswith("    return filename"):
            append = True

    with open(prepare_py, 'w') as f:
        f.writelines(lines)

def check_patch_status(pip_install_folder: str) -> bool:
    pass


if __name__ == "__main__":
    current_target_pip = locate_current_pip_folder()
    prepare_file = locate_target_file(current_target_pip)
    
    if not check_patch_status(current_target_pip):
        patch_target_file(prepare_file)

    pass

    # check the pip version, ensure it is in compat matrix
    # find the current pip site-packages folder
    # track down the specific file
    # look for backed up original file
        # if present, we're patched and we need to do nothing
        # if unpatched:
            # backup relevant file
            # replace relevant file

    # eventually this script should have two commands
    # drain to patch
    # plug to unpatch