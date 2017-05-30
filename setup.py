from setuptools import setup
from jacoren import (
    __version__ as version,
    __title__ as title,
    __description__ as description,
    __author__ as author,
    __author_email__ as author_email,
    __license__ as license,
)

# Requirements
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()


setup(
    name=title,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    license=license,
    packages=['jacoren'],
    package_dir={'jacoren': 'jacoren'},
    install_requires=requirements,
    entry_points = {
        'console_scripts': ['jacoren=jacoren._server:main'],
    }
)
