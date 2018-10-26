import os
import shutil
import sys
import re


def create_app(app_name, create_on_curdir=False):

    path = _template_path()

    print(f'\nCreating a new application: {app_name}')

    root_dir = os.path.join(os.curdir, app_name
                            if not create_on_curdir
                            else '')

    tpl_dir = os.path.join(root_dir, 'templates')
    ctrl_dir = os.path.join(root_dir, 'controllers')

    try:
        if not create_on_curdir:
            os.makedirs(tpl_dir)
            os.mkdir(ctrl_dir)
        else:
            os.mkdir('templates')
            os.mkdir('controllers')

    except OSError:
        print(('Error: the folder you are trying to create the app '
               f'`{app_name}` already exist'), file=sys.stderr)
        sys.exit()

    except FileExistsError as e:
        print(e, file=sys.stderr)
        sys.exit()

    shutil.copy(os.path.join(path, 'app.py'), root_dir)
    shutil.copy(os.path.join(path, 'index.html'), tpl_dir)
    shutil.copy(os.path.join(path, 'apiController.py'), ctrl_dir)

    app_created = (
            '\nYou are all set!!!\n\n'
            'To start your app:\n'
            '{}'
            '  $ python app.py\n\n'
            '  Browse to http://localhost:8000').format(f'  $ cd {app_name}\n'
                                                        if not create_on_curdir
                                                        else '')

    print(app_created)


def create_ctrl(ctrl_name):
    path = _template_path()

    ctrl_dir = os.path.join(os.curdir, 'controllers')

    if not os.path.exists(ctrl_dir):
        os.makedirs(ctrl_dir)

    formatted_ctrl_name = _get_ctrl_name(ctrl_name)

    if not formatted_ctrl_name:
        print(('error: invalid controller name `{}`. '
               'Controler names cannot contain '
               '`-` or `_`\n').format(ctrl_name))
        sys.exit()

    new_ctrl_path = os.path.join(ctrl_dir, formatted_ctrl_name)

    print(f'\nCreating a new controller: {formatted_ctrl_name}')

    if os.path.exists(new_ctrl_path):
        print((f'error: a controller named `{formatted_ctrl_name}`'
               ' already exist'), file=sys.stderr)
        sys.exit()

    shutil.copy(os.path.join(path, 'apiController.py'), new_ctrl_path)

    print((f'Controller `{formatted_ctrl_name}` '
           'has been successfully created\n'))


def _get_ctrl_name(ctrl_name):
    if re.search(r'(\-|\_)', ctrl_name):
        return None

    ctrl_name = re.sub('.py', '', ctrl_name)
    ctrl_name = re.split('controller', ctrl_name, flags=re.IGNORECASE)[0]

    return f'{ctrl_name}Controller.py'


def _template_path():
    path, _ = os.path.split(__file__)
    return os.path.join(path, '..', 'app_templates')
