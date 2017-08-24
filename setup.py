from distutils.core import setup

setup(
    name='Pyterrier',
    version='0.1.0',
    author='Daniel Furtado',
    author_email='daniel@dfurtado.com',
    packages=['pyterrier', 'pyterrier.http'],
    description='Micro web framework for Python 3',
    install_requires=[
        "Jinja2 == 2.8",
        "nose == 1.3.7",
        "Django == 1.11.4",
    ],
)
