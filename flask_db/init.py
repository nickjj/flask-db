import pathlib
import os

from shutil import copy
from distutils.dir_util import copy_tree


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
existing_files = []
copied_files = []


def cp_path(src, dst):
    src = os.path.join(TEMPLATE_PATH, src)

    if os.path.isfile(src):
        # We never want to clobber or disrupt existing files that may exist.
        if os.path.exists(dst):
            dst = append_new_extension(dst)

        result = copy(src, dst)
        copied_files.append(dst)
    else:
        result = copy_tree(src, dst)

    return result


def append_new_extension(path):
    new_path = f"{path}.new"
    existing_files.append((path, new_path))

    return new_path


def replace_in_file(path, search, replace):
    if not os.path.exists(path):
        return None

    with open(path, "r") as file:
        content = file.read()

    content = content.replace(search, replace)

    with open(path, "w") as file:
        file.write(content)

    return content


def file_depth_count(path):
    dir = os.path.dirname(path)
    depth_count = len(dir.split(os.path.sep))

    return depth_count


def alembic_ini_dst_path(path):
    path = os.path.join(path, "alembic.ini")

    return pathlib.Path(path).parents[file_depth_count(path)]


def mkdir_init(path):
    try:
        pathlib.Path(path).mkdir(parents=True)

        return f"{path} was created successfully"
    except FileExistsError:
        return None


def generate_configs(path, current_app_import_name):
    if mkdir_init(path) is None:
        print(f"Aborting! {path} already exists")
        return None, None

    cp_path("db", path)
    cp_path("alembic.ini",
            os.path.join(alembic_ini_dst_path(path), "alembic.ini"))

    replace_in_file("alembic.ini", "SCRIPT_LOCATION", path)
    replace_in_file("alembic.ini.new", "SCRIPT_LOCATION", path)
    replace_in_file(os.path.join(path, "env.py"),
                    "CURRENT_APP_IMPORT_NAME", current_app_import_name)
    replace_in_file(os.path.join(path, "env.py"), "  # noqa: E999", "")

    return copied_files, existing_files
