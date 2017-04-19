from argparse import ArgumentParser
import sys

from .cli.commands import create_app, create_ctrl

parser = ArgumentParser(prog='pyterrier', description='PyTerrier CLI')

parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 1.0')

parser.add_argument('-c', '--currentdir',
                    action='store_true',
                    dest='create_on_curdir',
                    default=False,
                    help=('specify whether or not scaffold the '
                          'application on the current directory.'))

parser.add_argument('--newapp',
                    type=str,
                    metavar='NAME',
                    dest='appname',
                    help='creates a new PyTerrier application')

parser.add_argument('--newcontroller',
                    type=str,
                    metavar='NAME',
                    dest='ctrlname',
                    help='creates a new controller')

args = vars(parser.parse_args())

appname = args.get('appname')
ctrlname = args.get('ctrlname')
create_on_curdir = args.get('create_on_curdir')

if appname is not None and ctrlname is not None:
    print(('pyterrier: error: --newapp and --newcontroller are not meant'
           ' to be used together.'))
    sys.exit()

if appname is not None:
    create_app(appname, create_on_curdir)
elif ctrlname is not None:
    create_ctrl(ctrlname)
