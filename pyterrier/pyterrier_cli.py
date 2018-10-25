import sys
import click

from pyterrier.cli.commands import create_app, create_ctrl


@click.command()
@click.option('--currentdir', is_flag=True)
@click.option('--newapp')
@click.option('--newcontroller')
def main(currentdir, newapp, newcontroller):
    if newapp is not None and newcontroller is not None:
        print(('pyterrier: error: --newapp and --newcontroller are not meant'
               ' to be used together.'))
        sys.exit()

    if newapp is not None:
        create_app(newapp, currentdir)
    elif newcontroller is not None:
        create_ctrl(newcontroller)


if __name__ == "__main__":
    sys.exit(main())
