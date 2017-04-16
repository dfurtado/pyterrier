import os
import shutil
import sys


def create_app(app_name, create_on_curdir=False):

    if create_on_curdir and len(os.listdir(os.curdir)) > 0:
        print("error: the current folder is not empty")
        sys.exit()

    path = _template_path()

    print(f"\nCreating a new application: {app_name}")

    root_dir = os.path.join(os.curdir, app_name if not create_on_curdir else "")
    tpl_dir = os.path.join(root_dir, "templates")
    ctrl_dir = os.path.join(root_dir, "controllers")

    try:
        if not create_on_curdir:
            os.makedirs(tpl_dir)
            os.mkdir(ctrl_dir)
        else:
            os.mkdir("templates")
            os.mkdir("controllers")

    except OSError:
        print(f"error: the folder you're trying to create the app `{app_name}` already exist", 
                file=sys.stderr)
        sys.exit()

    except FileExistsError as e:
        print(e, file=sys.stderr)
        sys.exit()

    shutil.copy(os.path.join(path, "app.py"), root_dir)
    shutil.copy(os.path.join(path, "index.html"), tpl_dir)
    shutil.copy(os.path.join(path, "apiController.py"), ctrl_dir)

    app_created = (
            "\nYou're all set!!!\n\n"
            "To start your app:\n"
            "{}"
            "  $ python app.py\n\n"
            "  Browse to http://localhost:8000").format(f"  $ cd {app_name}\n" 
                    if not create_on_curdir else "")

    print(app_created)


def create_ctrl(ctrl_name):
    print(f"Creating a new controller: Not implemented")


def _template_path():
    path, _ = os.path.split(__file__)
    return os.path.join(path, "..", "app_templates")
