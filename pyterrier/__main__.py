from argparse import ArgumentParser
import sys

from cli.commands import create_app, create_ctrl

parser = ArgumentParser(prog="pyterrier", description="PyTerrier CLI")

parser.add_argument("-v", "--version", action="version", version='%(prog)s 1.0')

parser.add_argument("--newapp", type=str, metavar="NAME", dest="appname",
                    help="Create a new PyTerrier application")

parser.add_argument("--newcontroller", type=str, metavar="NAME", dest="ctrlname",
                    help="Creates a new controller")

args = vars(parser.parse_args())

appname = args.get("appname")
ctrlname = args.get("ctrlname")

if appname != None and ctrlname != None:
    print(f"pyterrier: error: --newapp and --newcontroller are not meant to be used together.")
    sys.exit()

if appname != None:
    create_app(appname)
elif ctrlname != None:
    create_ctrl(ctrlname)





